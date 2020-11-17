import telebot
import mpu.io
import os
import sys
import json
import re
from telebot import types
import ccxt
import time
from time import sleep
from numbers import Number

#f = open("telegram_api.conf", "r")
bot = telebot.TeleBot('1335506716:AAHNYsWEra16d9RkExKS8vgSH5gg07ZSHJY')

exchange = None
key = ""
secret = ""
exchange_fee = 0.1
data = {}

example_signal_post = "#Format\nONLY FORWARD (NO TYPING)\n\nBy default Levarage is 5 and risk is 1 percent of portfolio.\nDo change accordingly\n\nFormat(leave Blank to know margin value):-\n **Entry:sl:Lev:Portfolio:risk:Margin** "
hellw = True

@bot.message_handler(content_types=["text"])
def hello_user(message):

    global example_signal_post
    global user
    if(hellw):
        user =  str(message.from_user.username)
        bot.send_message(
            message.from_user.id,
            "Hi "
            + str(message.from_user.username) + ""
           
        )
    
    bot.send_message(message.from_user.id, example_signal_post)
    bot.register_next_step_handler(message, get_forward)


def get_forward(message):

    signals_data = message.text
    msz = signals_data
    if ((signals_data.count(':')== 5) or (message.text == "/restart")):
        if message.text == "/restart":
            restart_bot(message)
        
        Entry = float(msz.split(':')[0])
        sLoss = float(msz.split(':')[1])
        Levrage = float(msz.split(':')[2])
        Port = float(msz.split(':')[3])
        risk = float(msz.split(':')[4])
        Margin  = msz.split(':')[5]
        slPercent = (abs(Entry - sLoss)*100) / Entry
        if(Levrage == ''):
                Levrage = 5
        slPercent = slPercent * Levrage
        if(Port == ''):
          print('Portfolio Please')
        if(risk == ''):
          risk = 1
        USDt = Port * (risk/100)
        global amount
        amount = (USDt / slPercent) * 100
        #print(amount)
        
        reply = "Hi " + user + " You can trade with " + str(amount) +"USDT \n\n Happy TraDing"
        bot.send_message(message.from_user.id, reply)
        hellw = False

def restart_bot(message):

    if message.text == "/restart" or True:
        bot.send_message(message.from_user.id, "Restart complete, send me /start")
        os.execl(sys.executable, sys.executable, *sys.argv)


bot.polling(none_stop=True, interval=0)
