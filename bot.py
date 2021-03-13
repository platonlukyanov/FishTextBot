import requests
import telebot
from databasecontrol import Controller
import os

def load_result(numberOfSentences, typeS):
    try:
        params = {
            "type": typeS,
            "number": numberOfSentences
        }
        url = "https://fish-text.ru/get"
        r = requests.get(url, params=params)

        frase = r.json()["text"]
        return frase
    except:
        return "ой... Что-то пошло не так"


token = os.environ.get("TOKEN")
bot = telebot.TeleBot(token)
filename = os.environ.get("DATABASENAME")
db_control = Controller(filename)


def write_data(message):
    try:
        db_control.write_user(
            message.from_user.id,
            message.from_user.first_name,
            message.from_user.last_name,
            message.from_user.username,
            message.from_user.language_code
        )
    except Exception as e:
        print("write user error: ", end="")
        print(e)

    try:
        db_control.write_message(message.message_id,
                                 message.from_user.id,
                                 message.date,
                                 message.text)
    except Exception as e:
        print("write message error: ", end="")
        print(e)


@bot.message_handler(commands=['start'])
def first_page(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Вдохновляющую фразу на день', callback_data="title"))
    markup.add(telebot.types.InlineKeyboardButton(text='Случайный текст', callback_data="sentence"))
    print("first page request. USER: ", message.from_user.id)

    write_data(message)
    bot.send_message(message.from_user.id, "Привет, что ты хотел-бы получить?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    typeS = call.data

    if typeS == "title":
        bot.send_message(call.message.chat.id, load_result(numberOfSentences=1, typeS="title"))
    else:
        bot.send_message(call.message.chat.id, "Сколько предложений?")


@bot.message_handler(content_types=['text'])
def numberator(message):
    print("Numberator. USER: ", message.from_user.id)
    write_data(message)
    if message.text.isdecimal():
        if int(message.text) <= 25:
            numS = message.text
            bot.send_message(message.from_user.id, load_result(numberOfSentences=int(numS), typeS="sentence"))
        else:
            bot.send_message(message.from_user.id, "У меня не такая большая фантазия( Попробуй попросить у меня текст длиной меньше 25 предложений.")
    else:
        bot.send_message(message.from_user.id, "Пишите цифрами! Если хотите начать напишите /start")


bot.polling(none_stop=True, interval=0)
