import os
import json
import telebot
from dotenv import load_dotenv
import requests as fetch

from helpers import set_interval

load_dotenv()
# constants
BOT_TOKEN = os.getenv("BOT_TOKEN")
COMPLIMENT_API = os.getenv("COMPLIMENT_API")
__dirname = os.path.dirname(os.path.abspath(__file__))
users_file = os.path.join(__dirname, "users.json")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

if not os.path.exists(users_file):
    with open(users_file, 'w') as file:
        data = {
            "users": []
        }
        json.dump(data, file, indent=3)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    f = open(users_file, "r")
    data = json.load(f)
    f.close()
    new_user = {
        "name": message.from_user.first_name,
        "username": message.from_user.username,
        "chat_id": message.chat.id,
    }

    if len(data["users"]) != 0:
        isFind = False
        for user in data["users"]:
            if user["chat_id"] == message.chat.id:
                isFind = True

        if not isFind:
            data["users"].append(new_user)
            f = open(users_file, "w+")
            json.dump(data, f, indent=3, ensure_ascii=False)

    else:
        data["users"].append(new_user)
        f = open(users_file, "w+")
        json.dump(data, f, indent=3, ensure_ascii=False)

    bot.send_message(message.chat.id, "Nice to meet you :)")


def compliment(username="LisavetaKrotova"):
    f = open(users_file, "r")
    data = json.load(f)
    f.close()
    sender_id = list(filter(lambda user: user["username"] == username, data["users"]))[0]["chat_id"]
    compliment_text = fetch.get(COMPLIMENT_API).json()
    bot.send_message(sender_id, compliment_text)


set_interval(compliment, 3)

bot.polling(none_stop=True)  # запуск бота
