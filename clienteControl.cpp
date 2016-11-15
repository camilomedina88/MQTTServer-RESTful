#include "mraa.hpp"
#include <iostream>
#include <unistd.h>
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mosquitto.h>
#include "mraa.hpp"
#include <pthread.h>
#include <string.h>

// Server connection parameters
#define MQTT_HOSTNAME "nickiler.ddns.net"
#define MQTT_PORT 1883
#define MQTT_USERNAME ""
#define MQTT_PASSWORD ""
#define MQTT_TOPIC "hello"
#define IDVAR_BOMBA "/solution/fad8397a-c934-48fa-8aee-7e6e4c2f5fd2/5a1bf940-3636-4223-8fc5-8f76bfccaae8/lv"
#define IDVAR_LEDS "/solution/fad8397a-c934-48fa-8aee-7e6e4c2f5fd2/a7b77b27-b5dc-4154-84e4-5810c9fc2928/lv"
#define IDVAR_VENTILADOR "/solution/fad8397a-c934-48fa-8aee-7e6e4c2f5fd2/44794d3e-b9e1-4f48-8fb9-2abf59270811/lv"

using namespace std;
char* estadoBomba;
int accionBomba, accionLeds, accionVentilador;
mraa::Gpio* bomba = new mraa::Gpio(8, true, false);
mraa::Gpio* leds = new mraa::Gpio(3, true, false);
mraa::Gpio* ventilador = new mraa::Gpio(7, true, false);
struct mosquitto *mosq1 = NULL;
struct mosquitto *mosq2 = NULL;
struct mosquitto *mosq3 = NULL;
char *host = "nickiler.ddns.net";
int port = 1883;
int keepalive = 60;
bool clean_session = true;

void deserialize(int topic, char * mensajeOriginal) {

	if (topic == 1) {
		sscanf(mensajeOriginal, "[{\"name\":\"bomba\",\"v\":%d}]",
				&accionBomba);
		cout << "Valor Bomba: " << accionBomba << endl;
	}

	//sscanf(mensajeOriginal,
	//	"[{\"name\":\"bomba\",\"v\":%d},{\"name\":\"leds\",\"v\":%d},{\"name\":\"ventilador\",\"v\":%d}]",
	//&accionBomba, &accionLeds, &accionVentilador);

	//cout << "Valor Leds: " << accionLeds << endl;
	//cout << "Valor ventilador: " << accionVentilador << endl;
}

void my_message_callback(struct mosquitto *mosq, void *userdata,
		const struct mosquitto_message *message) {
	if (message->payloadlen) {
		//printf("%s %s\n", message->topic, message->payload);

		string msjRecibido = (string) message->topic;
		//int comparacionTest = msjRecibido.compare(IDVAR_BOMBA);
		//cout << "Comparando este es:  " << comparacionTest << endl;

		int esBomba =msjRecibido.compare(IDVAR_BOMBA) ;
		int esVentilador =msjRecibido.compare(IDVAR_VENTILADOR) ;
		int esLeds = msjRecibido.compare(IDVAR_LEDS);
/*
		int esBomba = strncmp(IDVAR_BOMBA, message->topic, 80);
		int esVentilador = strncmp(IDVAR_LEDS, message->topic, 80);
		int esLeds = strncmp(IDVAR_VENTILADOR, message->topic, 80);
*/
		cout << endl << "---" << endl;
		if (esBomba == 0) {
			sscanf((char *) message->payload, "%d", &accionBomba);
			cout << "LA ACCION DE LA BOMBA ES: " << accionBomba << endl;
			bomba->write(accionBomba);

		}

		if (esVentilador == 0) {
			sscanf((char *) message->payload, "%d", &accionVentilador);
			cout << "LA ACCION DEL VENTILADOR ES: " << accionVentilador << endl;
			ventilador->write(accionVentilador);
		}

		if (esLeds==0) {
			sscanf((char *) message->payload, "%d", &accionLeds);
			cout << "LA ACCION DEL LEDS ES: " << accionLeds << endl;
			leds->write(accionLeds);
		}

		printf("-------------- \n");


		esBomba=2;
		esVentilador=2;
		esLeds=2;
	} else {
		printf("%s (null)\n", message->topic);
	}
	fflush(stdout);
}

void my_connect_callback(struct mosquitto *mosq, void *userdata, int result) {
	int i;
	if (!result) {
		/* Subscribe to broker information topics on successful connect. */

		mosquitto_subscribe(mosq, NULL, IDVAR_BOMBA, 2);
		mosquitto_subscribe(mosq, NULL, IDVAR_VENTILADOR, 2);
		mosquitto_subscribe(mosq, NULL, IDVAR_LEDS, 2);
	} else {
		fprintf(stderr, "Connect failed\n");
	}
}

void my_subscribe_callback(struct mosquitto *mosq, void *userdata, int mid,
		int qos_count, const int *granted_qos) {
	int i;

	printf("Subscribed (mid: %d): %d", mid, granted_qos[0]);
	for (i = 1; i < qos_count; i++) {
		printf(", %d", granted_qos[i]);
	}
	printf("\n");
}

void my_log_callback(struct mosquitto *mosq, void *userdata, int level,
		const char *str) {
	/* Pring all log messages regardless of level. */
	printf("%s\n", str);
}

int main(int argc, char **argv) {
	char *host = "nickiler.ddns.net";
	int port = 1883;
	int keepalive = 60;
	bool clean_session = true;

	//BOMBA
	//mraa::Gpio* bomba = new mraa::Gpio(8, true, false);
	if (bomba == NULL) {
		std::cerr << "Can't create mraa::Gpio object, exiting" << std::endl;
		return mraa::ERROR_UNSPECIFIED;
	}
	// set the pin as output
	if (bomba->dir(mraa::DIR_OUT) != mraa::SUCCESS) {
		std::cerr << "Can't set digital pin as output, exiting" << std::endl;
		return MRAA_ERROR_UNSPECIFIED;
	}

	//LEDS

	//mraa::Gpio* leds = new mraa::Gpio(3, true, false);
	if (leds == NULL) {
		std::cerr << "Can't create mraa::Gpio object, exiting" << std::endl;
		return mraa::ERROR_UNSPECIFIED;
	}
	// set the pin as output
	if (leds->dir(mraa::DIR_OUT) != mraa::SUCCESS) {
		std::cerr << "Can't set digital pin as output, exiting" << std::endl;
		return MRAA_ERROR_UNSPECIFIED;
	}

	// Ventilador

	//mraa::Gpio* ventilador = new mraa::Gpio(7, true, false);
	if (ventilador == NULL) {
		std::cerr << "Can't create mraa::Gpio object, exiting" << std::endl;
		return mraa::ERROR_UNSPECIFIED;
	}
	// set the pin as output
	if (ventilador->dir(mraa::DIR_OUT) != mraa::SUCCESS) {
		std::cerr << "Can't set digital pin as output, exiting" << std::endl;
		return MRAA_ERROR_UNSPECIFIED;
	}

	mosquitto_lib_init();
	mosq1 = mosquitto_new(NULL, clean_session, NULL);
	if (!mosq1) {
		fprintf(stderr, "Error: Out of memory.\n");
		return 0;
	}
	mosquitto_log_callback_set(mosq1, my_log_callback);
	mosquitto_connect_callback_set(mosq1, my_connect_callback);
	mosquitto_message_callback_set(mosq1, my_message_callback);
	mosquitto_subscribe_callback_set(mosq1, my_subscribe_callback);

	if (mosquitto_connect(mosq1, host, port, keepalive)) {
		fprintf(stderr, "Unable to connect.\n");
		return 0;
	}

	mosquitto_loop_forever(mosq1, -1, 1);
	mosquitto_destroy(mosq1);
	mosquitto_lib_cleanup();
	return 0;

	return 0;
}

