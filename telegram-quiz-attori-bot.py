import telebot
from mysql import connector
import random
import os
from flask import Flask, request

TOKEN = '1544405331:AAGeXsgA384zMu3Xfpd-y4nkUFZ0LR4XGeY'
URL = 'https://murmuring-tor-01816.herokuapp.com/' + TOKEN
PATH = os.path.join(os.getcwd(), 'Immagini')

bot = telebot.TeleBot(token = TOKEN, threaded = False)
bot.remove_webhook()
bot.set_webhook(url = URL)

app = Flask(__name__)

@app.route('/' + TOKEN, methods = ['POST'])
def webhook():
    
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))

    bot.process_new_updates(updates = [update])

    return 'ok', 200

@bot.message_handler(commands = ['start', 'help'])
def start(message):

    bot.send_message(text = 'Benvenuto\n In questo quiz cercherai di indovinare gli attori nelle immagini!', chat_id = message.chat.id)


@bot.message_handler(commands = ['contact'])
def start(message):

    bot.send_message(text = 'occo', chat_id = message.chat.id)

if __name__ == '__main__':
    
    app.run(host = '0.0.0.0', port = int(os.environ.get('PORT', 5000)))