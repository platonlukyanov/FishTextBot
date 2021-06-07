import telebot
from databasecontrol import Controller
from utils import write_data, load_result, get_wiki_message, send_wiki
from config import TOKEN
import os

token = TOKEN
bot = telebot.TeleBot(token)
filename = "botdb.db"
db_control = Controller(filename)


@bot.message_handler(commands=['start'])
def first_page(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Вдохновляющую фразу на день 😄', callback_data="title"))
    markup.add(telebot.types.InlineKeyboardButton(text='Случайный текст 🎲', callback_data="sentence"))
    markup.add(telebot.types.InlineKeyboardButton(text='Статья из Википедии 📖', callback_data="wiki"))
    print("first page request. USER: ", message.from_user.id)

    write_data(message)
    bot.send_message(message.from_user.id, "Привет, что ты хотел-бы получить?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    typeS = call.data

    if typeS == "title":
        bot.send_message(call.message.chat.id, load_result(numberOfSentences=1, typeS="title"))
    elif typeS == "sentence":
        bot.send_message(call.message.chat.id, "Сколько предложений?")
    elif typeS == "wiki":
        send_wiki(bot, call.message.chat.id)


@bot.message_handler(commands=["wiki"])
def wiki_handler(message):
    send_wiki(bot, message.from_user.id)


@bot.message_handler(commands=["text"])
def send_random_text_question(message):
    bot.send_message(message.from_user.id, "Сколько предложений?")


@bot.message_handler(commands=["phrase"])
def send_random_text_question(message):
    bot.send_message(message.from_user.id, load_result(numberOfSentences=1, typeS="title"))


@bot.message_handler(content_types=['text'])
def numberator(message):
    print("Numberator. USER: ", message.from_user.id)
    write_data(message)
    if message.text.isdecimal():
        if int(message.text) <= 25:
            numS = message.text
            bot.send_message(message.from_user.id, load_result(numberOfSentences=int(numS), typeS="sentence"))
        else:
            bot.send_message(message.from_user.id,
                             "У меня не такая большая фантазия( Попробуй попросить у меня текст длиной меньше 25 предложений.")
    else:
        bot.send_message(message.from_user.id, "Пишите цифрами! Если хотите начать напишите /start")


bot.polling(none_stop=True, interval=0)
