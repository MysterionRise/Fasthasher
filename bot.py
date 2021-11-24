import hashlib
import random
from string import ascii_letters
from time import sleep

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram.ext.dispatcher import run_async

import settings

hello = "ju57 7ry 70 b347 my h45h3r! y0u mu57 h45h 7h3 57r1n65"
flag_prefix = "CODEBERRY_CTF"
timeout = 1
dict_of_challengers = {}
solved_flags = {}


@run_async
def bot_help(update, context):
    chat_id = update.message.chat.id
    context.bot.send_message(
        chat_id,
        text="""
        <b>Codeberry Club Bot Commands:</b>
        
        <b>You could submit flag by simply sending it to the bot</b>
        
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
        sorted(dict_of_challengers.items(), key=lambda item: item[1])
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
    hashed = hashlib.sha256(update.message.text.encode("utf-8")).hexdigest()
    message = update.message.text
    print(message)
    try:
        print(hashed)
        if message == hashed:
            print("Success")
            update.message.reply_text(settings.FLAG1)
    except Exception as e:
        print(e)
    rand = "".join(random.choice(ascii_letters) for _ in range(20))
    hashed = hashlib.sha256(rand.encode()).hexdigest()
    update.message.reply_text(rand)
    sleep(timeout)
    chat_id = update.message.chat.id
    context.bot.send_message(
        chat_id,
        text="""
                                TOO SLOW!
                                The answer is {}
                                """.format(
            hashed
        ),
        parse_mode="HTML",
    )


def main():
    updater = Updater(settings.AUTH_TOKEN, use_context=True)
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
