__author__ = "Benedict Thompson"
__version__ = "0.1p"

import abc

from automod.chatbot import ChatBot


class ChatBase(abc.ABC):
    def __init__(self, chat_bot: ChatBot) -> None:
        ...

    @abc.abstractmethod
    def broadcast_message(self, ch_name:str, message: str) -> None:
        ...

    @abc.abstractmethod
    def send_message_to(self, user_id: str, message: str) -> None:
        ...

    @abc.abstractmethod
    def send_ban_req(self, user_id: str, reason: str = None) -> bool:
        ...

    @abc.abstractmethod
    def send_mute_req(self, user_id: str, ch_name: str, reason: str = None) -> bool:
        ...
