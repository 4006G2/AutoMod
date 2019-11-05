__author__ = "Benedict Thompson"
__version__ = "0.1p"

import automod.chatbot.chatbot as cb
from automod.chat.chat_discord import ChatDiscord
import csv
import os

file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keys.txt')
with open(file) as csvfile:
    data = csv.reader(csvfile)
    for row in data:
        line = row[0].split(':')
        if line[0] == "discord":
            Discord_Token = line[1]


def run():
    chat_bot = cb.ChatBot()
    platform = ChatDiscord(chat_bot, Discord_Token)
    platform.client.loop.create_task(platform.tasks())
    platform.client.run(platform.token)
