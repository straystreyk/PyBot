import os
import json
import telebot
import requests as fetch

api_token = "5290171127:AAF8M4LIx-JgKx1JZByBOUjwlxSoIj3DUM0"
api_compliments = "https://8768zwfurd.execute-api.us-east-1.amazonaws.com/v1/compliments"
__dirname = os.path.dirname(os.path.abspath(__file__))
users_file = os.path.join(__dirname, "users.json")
bot = telebot.TeleBot(api_token, parse_mode=None)

if not os.path.exists(users_file):
    with open(users_file, 'w') as file:
        data = {
            "users": []
        }
        json.dump(data, file)


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
            print(isFind)
            data["users"].append(new_user)
            f = open(users_file, "w+")
            json.dump(data, f)

    else:
        data["users"].append(new_user)
        f = open(users_file, "w+")
        json.dump(data, f)

    bot.send_message(message.chat.id, "Nice to meet you :)")


@bot.message_handler(commands=["compliment"])
def compliment(message):
    compliment_text = fetch.get(api_compliments).json()
    bot.send_message(message.chat.id, compliment_text)


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)  # запуск бота
    except Exception as e:
        print(e)