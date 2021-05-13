import telebot
import markovify
from misc import bot_db

with open("parse_birth.txt", encoding='utf-8') as f:
    text = f.read()
text_model = markovify.Text(text)

last_mess = ""


@bot_db.message_handler(commands=["birth"])
def start_message(message):
    global last_mess
    i = 0
    mess = ""
    while i != 5:
        sentence = text_model.make_short_sentence(120)
        if sentence is not None:
            mess += sentence + " "
            i += 1
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row('👍', '👎')
    bot_db.send_message(message.chat.id, mess, reply_markup=keyboard)
    last_mess = mess


@bot_db.message_handler(content_types=['text'])
def start_reply(message):
    global last_mess
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row('👍', '👎')

    if message.text == '👍':
        g = open('cards_birth_ai.csv', 'a')
        g.write(last_mess + '\n')
        g.close()
        bot_db.send_message(message.chat.id, "Поздравление добавлено в базу!")
    elif message.text == '👎':
        bot_db.send_message(message.chat.id, "Поздравление пропущено.")

    i = 0
    mess = ""
    while i != 5:
        sentence = text_model.make_short_sentence(120)
        if sentence is not None:
            mess += sentence + " "
            i += 1
    bot_db.send_message(message.chat.id, mess, reply_markup=keyboard)
    last_mess = mess
