import paho.mqtt.client as paho
import time
import json

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

			



def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/solution/4ce2b51d-e554-4735-917f-19ce54518934")

def on_publish(client, userdata, mid):
    #print("mid: "+str(mid))
    print(" ")
 

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    #infoGalileo=json.loads(str(msg.payload), object_hook=object_decoder)
    infoGalileo=json.loads(str(msg.payload))

    temperaturas=infoGalileo['0e33b708-b583-4a67-8021-c040374d5051']
    luzdatos=infoGalileo['ee7d96a9-7d52-42fe-9089-796a4811fec2']
    humedades=infoGalileo['e7737df9-081f-482d-931d-ca2b1f49d19f']
    #Mandar los tres anteriores a DB


    valorTemperatura=temperaturas[0]['v']
    valorLuz=luzdatos[0]['v']
    valorHumedad=humedades[0]['v']
    print("1.Valor Actual Humedad:")
    print(valorHumedad)
    print("2. Valor Actual Temperatura")
    print(valorTemperatura)
    print("3. Valor Actual Luz")
    print(valorLuz)
    eventos("hum",valorHumedad)
    eventos("temp",valorTemperatura)
    eventos("luz",valorLuz)

    


    #pruebajson=json.dumps([{'name': "bomba", 'v': bombaout},{'name': "leds", 'v': 0},{'name': "ventilador", 'v': 0}], separators=(',',':'))
    #print(pruebajson)
    #(rc, mid) = client.publish("/solution/edison1", pruebajson, qos=1)
    time.sleep(2)




client = paho.Client()
client.on_publish = on_publish
client.on_message = on_message
client.on_connect = on_connect
client.connect("nickiler.ddns.net", 1883)


client.loop_forever()
