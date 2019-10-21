__author__ = "Benedict Thompson"
__version__ = "0.1p"

import automod.chatbot.chatbot as cb


def run():
    chat_bot = cb.ChatBot()

    print(chat_bot.on_message("Ben", "Hello"))
