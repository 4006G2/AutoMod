import discord
import asyncio
from discord.ext import tasks, commands

from automod.chat import ChatDiscord
from automod.chatbot import ChatBot

TOKEN = 'NjM1OTU2MTQ2ODUwNzU4NjY2.Xa8FCQ.fajiq3kR39PXiPAwKbhYD5f3WfI'

GENERAL_C_ID = 635958836481622021
GUILD_ID = 635958836481622016

client = discord.Client()
general_channel = client.get_channel(GENERAL_C_ID)
# automod_srvr = client.guilds[0]
cb = ChatBot()
srvr = ChatDiscord(cb, TOKEN)
