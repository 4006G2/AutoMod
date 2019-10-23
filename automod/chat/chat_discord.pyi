from automod.chatbot import ChatBot
from . import ChatBase
from discord import Client


class ChatDiscord(ChatBase):

    def __init__(self, chat_bot: ChatBot, token: str) -> None:
        super().__init__(chat_bot)
        self.chat_bot: ChatBot = chat_bot
        self.token: str = token
        self.client: Client = Client()

    def find_user_id(self, user_name: str) -> int:

    def broadcast_message(self, message: str) -> None:
        ...

    def send_message_to(self, user_id: str, message: str) -> None:
        ...

    def send_ban_req(self, user_id: str, reason: str = None) -> bool:
        ...

    def send_mute_req(self, user_id: str, reason: str = None) -> bool:
        ...
