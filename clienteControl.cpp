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

// Server connection parameters
#define MQTT_HOSTNAME "nickiler.ddns.net"
#define MQTT_PORT 1883
#define MQTT_USERNAME ""
#define MQTT_PASSWORD ""
#define MQTT_TOPIC "hello"
using namespace std;
char* estadoBomba;
int accionBomba, accionLeds, accionVentilador;
mraa::Gpio* bomba = new mraa::Gpio(8, true, false);
mraa::Gpio* leds = new mraa::Gpio(3, true, false);
mraa::Gpio* ventilador = new mraa::Gpio(7, true, false);

void deserialize(char * mensajeOriginal) {

	sscanf(mensajeOriginal,
			"[{\"name\":\"bomba\",\"v\":%d},{\"name\":\"leds\",\"v\":%d},{\"name\":\"ventilador\",\"v\":%d}]",
			&accionBomba, &accionLeds, &accionVentilador);
	cout << "Valor Bomba: " << accionBomba << endl;
	cout << "Valor Leds: " << accionLeds << endl;
	cout << "Valor ventilador: " << accionVentilador << endl;
}

void my_message_callback(struct mosquitto *mosq, void *userdata,
		const struct mosquitto_message *message) {
	if (message->payloadlen) {
		printf("%s %s\n", message->topic, message->payload);
		estadoBomba = (char*) message->payload;
		deserialize(estadoBomba);
		if (accionBomba == 1) {
			bomba->write(1);
			cout << "Prendio Bomba" << endl;
		}
		if (accionBomba == 0) {
			bomba->write(0);
			cout << "Apago Bomba" << endl;
		}

		if (accionLeds == 1) {
			leds->write(1);
			cout << "Prendio Leds" << endl;
		}

		if (accionLeds == 0) {
			leds->write(0);
			cout << "Apago Leds" << endl;
		}

		if (accionVentilador == 1) {
			ventilador->write(1);
			cout<<"Prendio Ventilador"<<endl;
		}
		if (accionVentilador == 0) {
			ventilador->write(0);
			cout<<"Apago Ventilador"<<endl;
		}

	} else {
		printf("%s (null)\n", message->topic);
	}
	fflush(stdout);
}

void my_connect_callback(struct mosquitto *mosq, void *userdata, int result) {
	int i;
	if (!result) {
		/* Subscribe to broker information topics on successful connect. */
		mosquitto_subscribe(mosq, NULL, "hello", 2);
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
	struct mosquitto *mosq = NULL;

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

	sleep(5);
	cout << "RELE" << endl;


	mosquitto_lib_init();
	mosq = mosquitto_new(NULL, clean_session, NULL);
	if (!mosq) {
		fprintf(stderr, "Error: Out of memory.\n");
		return 1;
	}
	mosquitto_log_callback_set(mosq, my_log_callback);
	mosquitto_connect_callback_set(mosq, my_connect_callback);
	mosquitto_message_callback_set(mosq, my_message_callback);
	mosquitto_subscribe_callback_set(mosq, my_subscribe_callback);

	if (mosquitto_connect(mosq, host, port, keepalive)) {
		fprintf(stderr, "Unable to connect.\n");
		return 1;
	}

	mosquitto_loop_forever(mosq, -1, 1);
	mosquitto_destroy(mosq);
	mosquitto_lib_cleanup();

	return 0;
}
