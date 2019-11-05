from automod.chatbot import ChatBot
from typing import List, Any
from . import ChatBase
from discord import Client, Guild


class ChatDiscord(ChatBase):

    def __init__(self, chat_bot: ChatBot, token: str) -> None:
        super().__init__(chat_bot)
        self.chat_bot: ChatBot = chat_bot
        self.token: str = token
        self.client: Client = Client()
        self.guilds: List[Guild] = ...

    def find_guild_id(self, guild_name) -> int:
        ...

    def find_channel_id(self, ch_name: str) -> int:
        ...

    def find_user_id(self, user_name: str) -> int:
        ...

    def broadcast_message(self, ch_name: str, message: str) -> None:
        ...

    def send_message_to(self, user_id: str, message: str) -> None:
        ...

    def send_ban_req(self, user_name: str, reason: str = None) -> None:
        ...

    def find_banned_user(self, name: str):
        ...

    def unban(self, user_name, reason: str = None) -> None:
        ...

    def send_mute_req(self, user_name: str, reason: str = None) -> None:
        ...

    async def on_message(self, message: Any) -> None:
        ...

    async def send_message_to_id(self, user_id, message):
        ...

    async def tasks(self):
        ...

    async def get_last_msg(self, ch_nameL: str) -> Any:
        ...
