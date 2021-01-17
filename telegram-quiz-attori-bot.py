import telebot
from mysql import connector
from random import randint
from datetime import datetime
import os
from random import randint


IP = '80.210.122.173'
PORTA = 3306
USER = '5AI.VOGLI'
PASSWORD = '26'
DATABASE = '5AI.VOGLI'


TOKEN = '1544405331:AAGeXsgA384zMu3Xfpd-y4nkUFZ0LR4XGeY'
URL = 'https://telegram-quiz-attori.herokuapp.com/' + TOKEN

bot = telebot.TeleBot(token = TOKEN, threaded = False)

connessione = connector.connect(host = IP, port = PORTA, user = USER, password = PASSWORD, database = DATABASE)

cursore = connessione.cursor()

cursore.execute('select count(*) from quiz')

dimensione = cursore.fetchone()[0]
    
ids = [i + 1 for i in range(dimensione)]

idQuiz = -1
nome = ''
aiuto = ''

@bot.message_handler(commands = ['start', 'help'])
def help(message):

    bot.send_message(message.chat.id, 'Scrivi /quiz per ricevere una nuova immagine da indovinare.\nScrivi /hint per un indizio')

@bot.message_handler(commands = ['quiz'])
def quiz(message):

    global ids, idQuiz, nome, aiuto

    if len(ids) == 0:

        bot.send_message(text = 'Hai indovinato tutti i nomi degli attori, complimenti mi hai battuto! Per rigiocare digita /quiz.', chat_id = message.chat.id)

        idQuiz = -1

        ids = [i + 1 for i in range(dimensione)]

    else:

        # Prendo un indice dal random, lo salvo e lo rimuovo per poi effettuare la query e prendere i dati
        i = randint(0, len(ids) - 1)
        
        cursore.execute('select * from quiz where idQuiz = {}'.format(ids[i]))
        
        idQuiz, nome, aiuto = cursore.fetchone()
        
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
 
    global ids, idQuiz

    if idQuiz != -1:

        if nome in message.text.lower():

            if len(ids):

                bot.send_message(text = 'Bravo! /quiz', chat_id = message.chat.id)
            
                ids.remove(idQuiz)

            else:

                bot.send_message(text = 'Hai indovinato tutti i nomi degli attori, complimenti mi hai battuto!', chat_id = message.chat.id)


        else:

            bot.send_message(text = 'Riprova!', chat_id = message.chat.id)
    
    else:

        bot.send_message(text = 'Per giocare scrivi: /quiz.', chat_id = message.chat.id)

    data, ora = str(datetime.utcfromtimestamp(message.date)).split()

    cursore.execute('insert into risposta values(null, "{}", "{}", "{}")'.format(data, ora, message.text))

    connessione.commit()

def start():

    bot.polling(none_stop = True, interval = 0.5)

if __name__ == '__main__':
    
    start()
    