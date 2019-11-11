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
        self.muted: dict = {}

    async def find_guild_id(self, guild_name: str) -> int:
        ...

    def find_channel_id(self, ch_name: str) -> int:
        ...

    def find_user_id(self, user_name: str) -> int:
        ...

    async def broadcast_message(self, ch_name: str, message: str) -> None:
        ...

    async def send_message_to(self, user_id: str, message: str) -> None:
        ...

    async def send_message_to_id(self, user_id: int, message: str) -> None:
        ...

    async def get_last_msg(self, ch_name: str) -> Any:
        ...

    async def send_ban_req(self, user_name: str, reason: str = None) -> None:
        ...

    async def find_banned_user(self, name: str) -> Any:
        ...

    async def print_banned(self) -> None:
        ...

    async def unban(self, user_name: str, reason: str = None) -> None:
        ...

    async def send_mute_req(self, user_name: str, reason: str = None) -> None:
        ...

    async def unmute(self, user_name: str) -> None:
        ...

    async def unmute_all(self, reason: str = None) -> None:
        ...

    def report_all(self) -> None:
        ...

    async def discussion_prompt(self) -> None:
        ...

    async def event_alert(self) -> None:
        ...

    async def on_ready(self) -> None:
        ...

    async def on_message(self, message: Any) -> None:
        ...

    async def tasks(self) -> None:
        ...
