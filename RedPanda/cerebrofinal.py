import paho.mqtt.client as paho
import time
import json
import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RedPanda.settings")
django.setup()

from django.db import models
from iot_hub.models import DataSource, Variable, Event, VarValue

bombaout=0
ledsout=0
ventiladorout=0

#{"indices":[1,1,0,5],"temp":[{"v":7.15,"ts":1479079506}],"lux":[{"v":224.00,"ts":1479079506}],"com":[{"t":0,"l":0,"c":0,"ts":0}],"hum":[{"v":224.00,"ts":1479079506},{"v":215.00,"ts":1479079476},{"v":0.00,"ts":0},{"v":0.00,"ts":0},{"v":0.00,"ts":0}]}

#def eventos(variableID,valorActual,valorSetpoint,tipoOperacion,targetDataSource,targetVarID):
def eventos(variableID,valorActual):


	if(variableID=="hum"):
		#Revisar si tiene tipo de operacion Traerla
		tipoOperacionMenor=1
		tipoOperacionMayor=1
		#Traer el valor del Setpoint
		valorSetpointBajo=30
		valorSetpointAlto=60
		#Traer el targetDataSource
		targetDataSource="fad8397a-c934-48fa-8aee-7e6e4c2f5fd2"
		#Traer el targerVarID
		targetVarID="5a1bf940-3636-4223-8fc5-8f76bfccaae8"
		accion=0		
		if(tipoOperacionMayor==1):
			if(valorActual>valorSetpointAlto):
				accion=0
				print("APAGAR BOMBA")
				(rc, mid) = client.publish("/solution/"+targetDataSource+"/"+targetVarID+"/lv", "0", qos=1)

		if(tipoOperacionMenor==1):
			if(valorActual<valorSetpointBajo):
				accion=1
				print("PRENDER BOMBA")
				(rc, mid) = client.publish("/solution/"+targetDataSource+"/"+targetVarID+"/lv", "1", qos=1)
					

	if(variableID=="temp"):
		tipoOperacionMenor=1
		tipoOperacionMayor=1

		valorSetpointBajo=13
		valorSetpointAlto=17

		targetDataSource="fad8397a-c934-48fa-8aee-7e6e4c2f5fd2"
		targetVarID="44794d3e-b9e1-4f48-8fb9-2abf59270811"
		accion=0
		if(tipoOperacionMayor==1):
			if(valorActual>valorSetpointAlto):
				accion=1
				print("Prender Ventilador")	
				(rc, mid) = client.publish("/solution/"+targetDataSource+"/"+targetVarID+"/lv", "1", qos=1)			
		if(tipoOperacionMenor==1):
			if(valorActual<valorSetpointBajo):
				accion=0
				print("Apagar Ventilador")
				(rc, mid) = client.publish("/solution/"+targetDataSource+"/"+targetVarID+"/lv", "0", qos=1)
	

	if(variableID=="luz"):
		tipoOperacionMenor=1
		tipoOperacionMayor=1
		valorSetpointBajo=100
		valorSetpointAlto=300
		targetDataSource="fad8397a-c934-48fa-8aee-7e6e4c2f5fd2"
		targetVarID="a7b77b27-b5dc-4154-84e4-5810c9fc2928"
		accion=0
		if(tipoOperacionMayor==1):
			if(valorActual>valorSetpointAlto):
				accion=0
				print("Apagar LEDS")
				(rc, mid) = client.publish("/solution/"+targetDataSource+"/"+targetVarID+"/lv", "0", qos=1)				
		if(tipoOperacionMenor==1):
			if(valorActual<valorSetpointBajo):
				accion=1
				print("Prender LEDS")
				(rc, mid) = client.publish("/solution/"+targetDataSource+"/"+targetVarID+"/lv", "1", qos=1)

def eventosTotales(valorActual,tarjetaDestino,variableDestino,operandos,setpoints,acciones):			

	i=0
	for j in operandos:
		if(j=="MT"):

			if(valorActual>setpoints[i]):
				valorAccion=str(acciones[i])
				print ("---- Mayor que:  ")
				(rc, mid) = client.publish("/solution/"+str(tarjetaDestino[i])+"/"+str(variableDestino[i])+"/lv", valorAccion, qos=1)

		if(j=="LT"):

			if(valorActual<setpoints[i]):
				valorAccion=str(acciones[i])
				print ("---- Menor que:  ")
				(rc, mid) = client.publish("/solution/"+str(tarjetaDestino[i])+"/"+str(variableDestino[i])+"/lv", valorAccion, qos=1)

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

    			if(len(PandaEventos)>0):
					eventosTotales(valorActual,tarjetaDestino,variableDestino,operandos,setpoints,acciones)
       	#filtro='data_variable=+nombreJson'
    	

client = paho.Client()
client.on_publish = on_publish
client.on_message = on_message
client.on_connect = on_connect
client.connect("nickiler.ddns.net", 1883)


client.loop_forever()
