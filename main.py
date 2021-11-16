import telebot
import time
import os
import random
from string import ascii_letters
from time import sleep
import hashlib
from token import token

flag = "zss{50_n1c3_h45h3r}"
bot = telebot.TeleBot(token)
timeout = 1
hello = "ju57 7ry 70 b347 my h45h3r! y0u mu57 h45h 7h3 57r1n65"
hashed = ""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, hello)

@bot.message_handler(func=lambda message: True)
def hasher(message):
    global hashed
    print(message.text)
    try:
        print(hashed)
        if message.text == hashed:
            bot.send_message(message.chat.id, flag)
            return
    except:
        pass
    rand = ''.join(random.choice(ascii_letters) for _ in range(15))
    hashed = hashlib.md5(rand.encode()).hexdigest()
    bot.send_message(message.chat.id, rand)
    sleep(timeout)
    bot.send_message(message.chat.id, "TOO SLOW!\nThe answer is " + hashed)
    hashed = ""

bot.polling()

