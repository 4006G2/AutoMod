from automod.chatbot import ChatBot
from . import ChatBase
from python_twitch_irc import TwitchIrc
from twitch import Helix



class ChatTwitch(ChatBase):

    def __init__(self, chat_bot: ChatBot, token: str) -> None:
        super().__init__(chat_bot)
        self.chat_bot: ChatBot = chat_bot
        self.token: str = token
        self.client: Helix = Helix



    def find_channel_id(self, ch_name: str) -> int:
        ...

    def find_user_id(self, user_name: str) -> int:
        ...

    def broadcast_message(self, ch_name: str, message: str) -> None:
        ...

    def send_message_to(self, user_id: str, message: str) -> None:
        ...

    def send_ban_req(self, user_id: str, reason: str = None) -> None:
        ...

    def find_banned_user(self, name: str):
        ...

    def unban(self, user_name, reason: str = None) -> None:
        ...

    def send_mute_req(self, user_id: str, reason: str = None) -> None:
        ...
