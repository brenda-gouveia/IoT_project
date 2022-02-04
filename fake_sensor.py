#*****************************************************************************************
#*Copyright (c) UFF - Federal Fluminense University 2022                                 *
#*                                                                                       *
#*Author(s): Brenda Gomes Gouveia <brendagouveia@id.uff.br>                              *
#*                                                                                       *
#*Esse arquivo faz parte de um projeto para a disciplina Internet das Coisas, ministrada *
#*pela professora Flávia Delicato.                                                       *
#*                                                                                       *
#*O arquivo simula sensores de temperatura e movimento. Os dados utilizados vem do       *
#*projeto WSU CASAS smart home da Washington State University.                           *
#*http://casas.wsu.edu/                                                                  *
#*****************************************************************************************
import socket
import time

def enviar(linha):
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(linha.encode(),("127.0.0.1",5555))# envia o dado coletado para o gateway
    

f = open("data.txt","r") 
linha = f.readline()# coleta os dados
while linha!='':
    print(linha)
    enviar(linha)
    linha=f.readline()
    time.sleep(5)
f.close()
