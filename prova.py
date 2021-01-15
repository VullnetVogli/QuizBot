from flask import Flask, request
import telebot

TOKEN = '1544405331:AAGeXsgA384zMu3Xfpd-y4nkUFZ0LR4XGeY'
URL = 'https://telegram-quiz-attori.herokuapp.com/'

server = Flask(__name__)

bot = telebot.TeleBot(token = TOKEN)

@bot.message_handler(content_types = ['text'])
def chat_message(message):
    
    bot.send_message(text = 'o', chat_id = message.chat.id)

@server.route('/{}'.format(TOKEN), methods=['POST'])
def getMessage():

    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    
    return "!", 200

@server.route("/")
def webhook():
    
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))

    bot.process_new_updates([update])
    
    return "!", 200
