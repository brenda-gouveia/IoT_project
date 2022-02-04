#**********************************************************************************************
#*Copyright (c) UFF - Federal Fluminense University 2022                                      *
#*                                                                                            *
#*Author(s): Brenda Gomes Gouveia                                                             *
#*                                                                                            *
#*Esse arquivo faz parte de um projeto da disciplina Internet das Coisas, ministrada pela     *
#*professora Flávia Delicato.                                                                 *
#*                                                                                            *
#*Esse arquivo é um gateway, que recebe informações do sensor_fake e envia para o broker      *
#**********************************************************************************************
import time
import socket
import paho.mqtt.publish as publish
import paho.mqtt.client as paho
from paho import mqtt

HOST=''
PORT=5555

mqtt_broker='broker.mqttdashboard.com' # utiliza o broker gratuito HIVEMQ
mqtt_port=1883
mqtt_topic='casa/comodos1' # tópico dos sensores de movimento
mqtt_topic2='casa/temperatura1'# tópico dos sensores de temperatura

#A ID dos nós sensores e onde estão localizados
quarto = ("M001","M002","M003","M005","M007")
salaestar=("M009","M010","M012","M013","M020")
cozinha=("M015","M017","M019","M018")
escritorio=("M027","M025","M026")
salajantar=("M014")
banheiro=("M029","M034","M004")

temperatura_quarto=("T001")
temperatura_sala=("T002")
temperatura_cozinha=("T003")
temperatura_escritorio=("T005")

def comodo(msg):
    x=msg.replace("\\t"," ")
    x=x.replace("'","")
    x=x.split(" ")
    
    if x[2] in quarto:
        x[2]="quarto"
        print("quarto")
        
    elif x[2] in salaestar:
        x[2]="sala_de_estar"
        print("sala_de_estar")
        
    elif x[2] in cozinha:
        x[2]="cozinha"
        print("cozinha")
        
    elif x[2] in escritorio:
        x[2]="escritorio"
        print("escritorio")
        
    elif x[2] in salajantar:
        x[2]="sala_de_jantar"
        print("sala_de_jantar")
        
    else:
        if x[2] in temperatura_quarto:
            x[2]="temperatura_quarto"
            
        elif x[2] in temperatura_sala:
            x[2]="temperatura_sala"
            
        elif x[2] in temperatura_cozinha:
            x[2]="temperatura_cozinha"
            
        else:
            x[2]="temperatura_escritorio"
            
        x[3]=x[3].replace("\\n","")
        
        print("temperatura")

    return x[0]+" "+x[1]+" "+x[2]+" "+x[3]

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))
    
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

def main():
    
    client = paho.Client()
    client.on_connect= on_connect
    # enable TLS for secure connection
    #client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    # set username and password
    #client.username_pw_set("admin", "123456")
    client.connect(mqtt_broker,mqtt_port) # se conecta ao broker
    client.loop_start()
    
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
        s.bind((HOST,PORT)) 
        print("Aguardando dados")
        while(1):          
            message,address=s.recvfrom(8192) #recebe as informações do sensor_fake
            if str(message).find("OFF")==-1: # filtra os nós que estão fora de alcance
               message=comodo(str(message)) # mapeia os sensores
               if message.find("temperatura")!=-1:
                   (rc,mid)= client.publish(mqtt_topic2,message,qos=1) # tópico temperatura
               else:
                   #tópico cômodos
                   (rc, mid) = client.publish(mqtt_topic, message, qos=1)
                
            time.sleep(5)

if __name__ == "__main__":
    main()