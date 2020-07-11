import telebot
from telebot import types
from monica import Chatbot
from database import DataBase
import time

uradb = DataBase()

while True:

    tkn = ""  # Requires the monica's chatbot token
    bot = telebot.TeleBot(tkn)

    monica = Chatbot()

    def req_monica(message):
        return True

    @bot.message_handler(commands=["start"])
    def start(message):
        global user
        bot.send_chat_action(message.chat.id, "typing")
        msg = "Olá! Eu sou a Mônica, a assistente virtual de Uberaba. Como posso te ajudar hoje?"
        bot.send_message(message.chat.id, msg)
        monica.user = uradb.get_telegram_user(message.chat.id)
        print(f"Usuário conectado: {monica.user[2]}")

    @bot.message_handler(func=req_monica)
    def monica_response(message):
        if not monica.user:
            monica.user = uradb.get_telegram_user(message.chat.id)
        bot.send_chat_action(message.chat.id, "typing")
        msg = monica.get_response(message.text)
        bot.send_message(message.chat.id, msg)

    try:
        print("Mônica: Olá! Já estou disponível no Telegram através do link https://t.me/ura_zbot.")
        bot.infinity_polling(True)
    except:
        data = time.localtime()
        print(f"Reconectando às {data.tm_hour}:{data.tm_min}:{data.tm_sec}")

