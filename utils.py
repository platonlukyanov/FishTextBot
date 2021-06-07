from databasecontrol import Controller
import requests
from wiki_parser import get_random_wiki


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


def get_wiki_message():
    message = ""
    random_wiki = get_random_wiki()
    title = random_wiki.get("title")
    body = random_wiki.get("body")[:4000]
    link = random_wiki.get("link")
    if not link:
        message += "*{}*\n\n".format(title)
    else:
        message += "\*\*\* [{}]({}) \*\*\* \n\n".format(title, link)
    message += body
    return message


def write_data(message, filename="botdb.db"):
    db_control = Controller(filename)
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


# Messages

def send_wiki(bot, chat_id):
    bot.send_message(chat_id, get_wiki_message(), parse_mode="markdown")