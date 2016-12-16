# coding=utf-8

import telebot # Importamos las librería
TOKEN = '302301685:AAHGQ9dLp1jywSOglr641_LE49pKNjRpi8I'
tb = telebot.TeleBot(TOKEN) # Combinamos la declaración del Token con la función de la API
tb.send_message("266748395", text="Temperatura: Alerta Nivel Alto!")

