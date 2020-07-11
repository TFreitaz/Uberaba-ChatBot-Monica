import telebot
from database import DataBase


uradb = DataBase()

tkn = ""  # Requires the Monica's chatbot token
bot = telebot.TeleBot(tkn)

msg_1 = "Alerta! Há um alagamento na Av. Leopoldino de Oliveira."
# msg_2 = "Alerta! Houve troca de tiros nesta madrugada. Não saia de casa."

msgs = [
    msg_1,
    # msg_2,
]

params = {"notification": "1"}
r = uradb.get_users(params)

for i in r:
    for msg in msgs:
        bot.send_message(i[2], msg)
