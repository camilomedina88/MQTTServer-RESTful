import paho.mqtt.client as paho
import time
import json
import os
import sys
import django
import telebot


TOKEN = '302301685:AAHGQ9dLp1jywSOglr641_LE49pKNjRpi8I'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RedPanda.settings")
django.setup()

from django.db import models
from iot_hub.models import DataSource, Variable, Event, VarValue

bombaout=0
ledsout=0
ventiladorout=0
tb = telebot.TeleBot(TOKEN)

#{"indices":[1,1,0,5],"temp":[{"v":7.15,"ts":1479079506}],"lux":[{"v":224.00,"ts":1479079506}],"com":[{"t":0,"l":0,"c":0,"ts":0}],"hum":[{"v":224.00,"ts":1479079506},{"v":215.00,"ts":1479079476},{"v":0.00,"ts":0},{"v":0.00,"ts":0},{"v":0.00,"ts":0}]}

#def eventos(variableID,valorActual,valorSetpoint,tipoOperacion,targetDataSource,targetVarID):

def eventosTotales(valorActual,tarjetaDestino,variableDestino,operandos,setpoints,acciones,tipoAccion,telegramID,keyJson):			
	#eventosTotales(valorActual,tarjetaDestino,variableDestino,operandos,setpoints,acciones,tipoAccion,telegramID)
	i=0
	for j in operandos:
		if(j=="MT"):

			if(valorActual>setpoints[i]):
				if(tipoAccion[i]=="SET"):
					valorAccion=str(acciones[i])
					print ("---- Mayor que:  ")
					(rc, mid) = client.publish("/solution/"+str(tarjetaDestino[i])+"/"+str(variableDestino[i])+"/lv", valorAccion, qos=1)
				
				if(tipoAccion[i]=="TEL"):
					tb.send_message(telegramID[i], text=keyJson+": ALARMA: Valor Alto")


		if(j=="LT"):

			if(valorActual<setpoints[i]):
				if(tipoAccion[i]=="SET"):
					valorAccion=str(acciones[i])
					print ("---- Menor que:  ")
					(rc, mid) = client.publish("/solution/"+str(tarjetaDestino[i])+"/"+str(variableDestino[i])+"/lv", valorAccion, qos=1)
				
				if(tipoAccion[i]=="TEL"):
					tb.send_message(telegramID[i], text=keyJson+": ALARMA: Valor bajo")

		if(j=="EQ"):

			print("IGUAL")


		i=i+1





def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/solution/4ce2b51d-e554-4735-917f-19ce54518934")

def on_publish(client, userdata, mid):
    #print("mid: "+str(mid))
    print(" ")
 

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    infoGalileo=json.loads(str(msg.payload))
    #Averiguar cual es UUID Origen
    llegaronLasVariables=infoGalileo.keys()


    for k in llegaronLasVariables:
    	#Saco el nombre del JSON
    	nombreJson=k
    	#Saco todos los elementos

    	elementosJson=infoGalileo[nombreJson]
    	print(elementosJson)
    	#Saco el valor actual
    	if(k != "indices"):
    		if(k != "com"):
    			
    			valorActual=elementosJson[0]['v']
    			
    			PandaEventos=Event.objects.filter(data_variable=nombreJson)
    			operandos=[]
    			setpoints=[]
    			tarjetaDestino=[]
    			variableDestino=[]
    			acciones=[]
    			telegramID=[]
    			tipoAccion=[]
    			print(k)
    			b=VarValue(value=str(valorActual),variable=Variable.objects.get(var_id = k))
    			print b
    			b.save()

    	
    			for event in PandaEventos:
    		
    				setpoints.append(event.compare_value)
    				operandos.append(event.operand)
    				tarjetaDestino.append(event.set_data_source.source_id)
    				variableDestino.append(event.set_data_variable.var_id)
    				acciones.append(event.value_set)
    				telegramID.append(event.telegram_id)
    				tipoAccion.append(event.action)

    			if(len(PandaEventos)>0):
					eventosTotales(valorActual,tarjetaDestino,variableDestino,operandos,setpoints,acciones,tipoAccion,telegramID,k)
       	#filtro='data_variable=+nombreJson'
    	

client = paho.Client()
client.on_publish = on_publish
client.on_message = on_message
client.on_connect = on_connect
client.connect("nickiler.ddns.net", 1883)


client.loop_forever()
