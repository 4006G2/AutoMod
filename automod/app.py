__author__ = "Benedict Thompson"
__version__ = "0.1p"

import automod.chatbot.chatbot as cb
from automod.chat.chat_discord import ChatDiscord

TOKEN = 'NjM1OTU2MTQ2ODUwNzU4NjY2.Xa8FCQ.fajiq3kR39PXiPAwKbhYD5f3WfI'


def run():
    chat_bot = cb.ChatBot()
    # print(chat_bot.on_message("Ben", "Hello"))
    platform = ChatDiscord(chat_bot, TOKEN)
    # read event file
    stop = False
    while not stop:
        platform.client.loop.create_task(platform.tasks())
        platform.client.run(platform.token)
