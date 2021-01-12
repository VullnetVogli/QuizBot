import telebot
from mysql import connector
import random
import os
from flask import Flask, request

TOKEN = '1544405331:AAGeXsgA384zMu3Xfpd-y4nkUFZ0LR4XGeY'
URL = 'https://api.telegram.org/bot{}/'.format(TOKEN)
PATH = os.path.join(os.getcwd(), 'Immagini')

bot = telebot.TeleBot(token = TOKEN, threaded = False)

app = Flask(__name__)

@app.route('/' + TOKEN, methods = ['POST'])
def webhook():
    
    bot.remove_webhook()
    
    bot.set_webhook(url = URL)

    return 'ok', 200

@bot.message_handler(commands = ['start'])
def start(message):

    bot.send_message(text = 'Benvenuto\n In questo quiz cercherai di indovinare gli attori nelle immagini!', chat_id = message.chat.id)

