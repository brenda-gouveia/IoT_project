#*****************************************************************************************
#*Copyright (c) UFF - Federal Fluminense University 2022                                 *
#*                                                                                       *
#*Author(s): Brenda Gomes Gouveia <brendagouveia@id.uff.br>                              *
#*                                                                                       *
#*Esse arquivo faz parte de um projeto da disciplina Internet das Coisas, ministrada pela*
#*professora Flávia Delicato                                                             *
#*                                                                                       *
#*O arquivo se inscreve nos tópicos, e envia-los para o InfluxDB                         *
#*****************************************************************************************
from fastapi import FastAPI
from paho import mqtt
from fastapi_mqtt import FastMQTT, MQTTConfig
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import datetime

mqtt_broker = 'broker.mqttdashboard.com'
mqtt_port = 1883
mqtt_topic = "casa/comodos1"
mqtt_topic2= "casa/temperatura1"
filenamet="temperatura.txt"
filenamec="comodo.txt"

app = FastAPI()

mqtt_config = MQTTConfig(host = mqtt_broker,port = mqtt_port,keepalive = 60)

mqtt = FastMQTT(config=mqtt_config)

mqtt.init_app(app)

token = "1MI7_9MBv6pDLHJKv9NDhmNFMCfaOK3s-6HFgCwRXyT2LM2d29Rtcq9QN0dV2oH-IbEmCh7mMzpvWqR7jSPedg=="
org = "UFF-Internet das Coisas"
bucket = "trabalho"

client = InfluxDBClient(url="http://localhost:8086", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe(mqtt_topic) #subscribing mqtt topic
    mqtt.client.subscribe(mqtt_topic2)
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)

    

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)
    
@mqtt.subscribe(mqtt_topic) 
async def get_dado(client,topic, payload, qos, properties): #recebe o tópico cômodos
    print("data: ", topic, payload.decode(), qos, properties)
    s=payload.decode()
    x=s.split(" ")
    data = "casa,comodo="+ x[2]+" valor=1" #converte para o protocolo em linha
    write_api.write(bucket, org, data) #envia para o InfluxDB

@mqtt.subscribe(mqtt_topic2)
async def get_temperatura(client,topic,payload,qos,properties):
    print("data: ", topic, payload.decode(), qos, properties)
    s=payload.decode()
    x=s.split(" ")
    data = "casa,temperatura="+ x[2]+" valor="+x[3] #converte para o protocolo em linha
    write_api.write(bucket, org, data) #envia para o InfluxDB


@app.get("/teste")
async def teste():
    return {"data"}
    
    
 