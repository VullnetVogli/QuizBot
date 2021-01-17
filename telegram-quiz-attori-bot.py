from flask import Flask, request
import telebot
from mysql import connector
from random import randint
from datetime import datetime
import os


IP = '80.210.122.173'
PORTA = 3306
USER = '5AI.VOGLI'
PASSWORD = '26'
DATABASE = '5AI.VOGLI'


TOKEN = '1544405331:AAGeXsgA384zMu3Xfpd-y4nkUFZ0LR4XGeY'
URL = 'https://telegram-quiz-attori.herokuapp.com/' + TOKEN

#server = Flask(__name__)

bot = telebot.TeleBot(token = TOKEN, threaded = False)
bot.remove_webhook()

connessione = connector.connect(host = IP, port = PORTA, user = USER, password = PASSWORD, database = DATABASE)

cursore = connessione.cursor()

idQuiz = -1
nome = ''
aiuto = ''

@bot.message_handler(commands = ['start', 'help'])
def help(message):

    bot.send_message(message.chat.id, 'Scrivi /quiz per ricevere una nuova immagine da indovinare.\nScrivi /hint per un indizio')

@bot.message_handler(commands = ['quiz'])
def quizz(message):

    global idQuiz, nome, aiuto

    cursore.execute('select count(*) from quiz')

    dimensione = cursore.fetchone()[0]
    
    cursore.execute('select * from quiz where idQuiz = {}'.format(randint(1, dimensione)))
    
    idQuiz, nome, aiuto = cursore.fetchone()

    print(idQuiz, nome, aiuto)

    bot.send_photo(photo = open('Immagini//{}.jpg'.format(idQuiz), 'rb'), caption = 'Chi è?', chat_id = message.chat.id)

@bot.message_handler(commands = ['hint'])
def hint(message):

    # Quando un utente vuole un aiuto per un quiz non ancora chiesto mando il messaggio di richiesta della immagine da indovinare
    if idQuiz == -1:

        bot.send_message(text = aiuto, chat_id = message.chat.id)    

    else:

        bot.send_message(text = aiuto, chat_id=message.chat.id)

@bot.message_handler(content_types = ['text'])
def chat_message(message):
    
    if idQuiz != -1:

        if nome in message.text.lower():

            bot.send_message(text = 'Bravo! /quiz', chat_id = message.chat.id)

        else:

            bot.send_message(text = 'Riprova!', chat_id = message.chat.id)
    
    else:

        bot.send_message(text = 'Per giocare scrivi: /quiz.', chat_id = message.chat.id)

    data, ora = str(datetime.utcfromtimestamp(message.date)).split()

    cursore.execute('insert into risposta values(null, "{}", "{}", "{}")'.format(data, ora, message.text))

    connessione.commit()
'''
@server.route('/{}'.format(TOKEN), methods=['POST'])
def getMessage():

    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    
    return "!", 200

@server.route("/")
def webhook():
    
    bot.remove_webhook()

    bot.set_webhook(url = URL)
    
    return "!", 200
'''
def start():

    bot.polling(none_stop = True, interval = 0.5)

if __name__ == '__main__':
    
    start()
    