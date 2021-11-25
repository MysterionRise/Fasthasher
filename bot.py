import hashlib
import os
import pickle
import random
from string import ascii_letters
from time import sleep

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram.ext.dispatcher import run_async

import settings

hello = "ju57 7ry 70 b347 my h45h3r! y0u mu57 h45h 7h3 57r1n65"
flag_prefix = "CODEBERRY_CTF"
timeout = 1
hashed_flags = {}


def read_statusboard():
    global dict_of_challengers
    if os.path.exists("dict_of_challengers"):
        with open("dict_of_challengers", "rb") as f:
            dict_of_challengers = pickle.load(f)
    else:
        dict_of_challengers = {}
    global solved_flags
    if os.path.exists("solved_flags"):
        with open("solved_flags", "rb") as f:
            solved_flags = pickle.load(f)
    else:
        solved_flags = {}


@run_async
def bot_help(update, context):
    chat_id = update.message.chat.id
    context.bot.send_message(
        chat_id,
        text="""
        <b>Codeberry Club Bot Commands:</b>
        
        <b>You could submit flag by simply sending it to the bot</b>
        
        <b>Challenge 1:</b>
        <i>Send /start command and reply to bot in order to continue</i>
        
        <b>Challenge 2:</b>
        <i>Junior team member got a task to obfuscate Spring Boot application</i>
        <i>However, it looks like something is wrong. Could you help?</i> 
        <i>https://drive.google.com/file/d/1i5s71QN9WbLDiMyajABKGPGS9gwqDCN8/view?usp=sharing</i>
        
        <b>Challenge 3:</b>
        <i>Your colleague is working on very important customer project and unfortunately, forgot the password to the admin page</i>
        <i>It could lead to a lot of problems. Could you help?</i>
        <i>http://ec2-54-246-224-31.eu-west-1.compute.amazonaws.com:8888/login</i>
        
        /help - show this help
        /statusboard - show current status of the challenge
        /start - start challenge
        """,
        parse_mode="HTML",
    )


@run_async
def start_challenge(update, context):
    chat_id = update.message.chat.id
    context.bot.send_message(
        chat_id, text="ju57 7ry 70 b347 my h45h3r! y0u mu57 h45h 7h3 57r1n65"
    )


@run_async
def submit_flag(update, context):
    message = update.message.text
    username = update.message.from_user["username"]
    if (
        message == settings.FLAG1
        or message == settings.FLAG2
        or message == settings.FLAG3
    ):
        solved = solved_flags.get(username, [])
        if message not in solved:
            print("Success")
            update.message.reply_text("c0rr3c7 fl46! c0n6r475!")
            dict_of_challengers[username] = dict_of_challengers.get(username, 0) + 100
            print(dict_of_challengers)
            solved_flags[username] = solved + [message]
            print(solved_flags)
        else:
            print("Already solved")
            update.message.reply_text("y0u r3 4lr34dy 607 7h15 fl46!")
    else:
        print("Fail")
        update.message.reply_text("wr0n6 fl46!")


def get_statusboard():
    result = ""
    for key, value in dict(
        sorted(dict_of_challengers.items(), key=lambda item: -item[1])
    ).items():
        result += "<b>{}</b> - {}\n".format(key, value)
    return result


@run_async
def statusboard(update, context):
    try:
        chat_id = update.message.chat.id
        context.bot.send_message(chat_id, text=get_statusboard(), parse_mode="HTML")
    except Exception as e:
        print(e)


@run_async
def fast_hasher(update, context):
    username = update.message.from_user["username"]
    message = update.message.text
    print(message)
    try:
        if message == hashed_flags.get(username, ""):
            print("Success")
            update.message.reply_text(settings.FLAG1)
    except Exception as e:
        print(e)
    rand = "".join(random.choice(ascii_letters) for _ in range(20))
    hashed = hashlib.sha256(rand.encode()).hexdigest()
    hashed_flags[username] = hashed
    update.message.reply_text(rand)
    sleep(timeout)
    chat_id = update.message.chat.id
    context.bot.send_message(
        chat_id,
        text="""TOO SLOW! The answer is {}""".format(hashed),
        parse_mode="HTML",
    )
    hashed_flags[username] = ""


def stop(signum, frame):
    with open("dict_of_challengers", "wb") as f:
        pickle.dump(dict_of_challengers, f)
    with open("solved_flags", "wb") as f:
        pickle.dump(solved_flags, f)


def main():
    read_statusboard()
    updater = Updater(settings.AUTH_TOKEN, user_sig_handler=stop, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("help", bot_help))
    updater.dispatcher.add_handler(CommandHandler("start", start_challenge))
    updater.dispatcher.add_handler(CommandHandler("statusboard", statusboard))
    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.text
            & ~Filters.command
            & ~Filters.regex(r"{}*".format(flag_prefix)),
            fast_hasher,
        )
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex(r"{}*".format(flag_prefix)), submit_flag)
    )
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
