__author__ = "Benedict Thompson"
__version__ = "0.1p"

import abc

from automod.chatbot import ChatBot


class ChatBase(abc.ABC):
    def __init__(self, chat_bot: ChatBot) -> None:
        super().__init__()
        self._chat_bot = chat_bot
        chat_bot.server = self

    @abc.abstractmethod
    def on_message_received(self, user_id: str, message: str) -> None:
        """
        called when a message is received from any user

        :param user_id: the id of the user sending the message
        :param message: the message sent
        :return: None
        """
        pass

    @abc.abstractmethod
    def broadcast_message(self, message: str) -> None:
        """
        Sends a message to all users in chat

        :param message: the message to be sent
        :return: None
        """
        pass

    @abc.abstractmethod
    def send_message_to(self, user_id: str, message: str) -> None:
        """
        Sends a message to a specific user (if possible)

        :param user_id:
        :param message:
        :return:
        """
        pass

    @abc.abstractmethod
    def send_ban_req(self, user_id: str, reason: str = None) -> bool:
        """
        sends a request to the server to ban the user

        :param user_id: the user_id to ban
        :param reason: reason for ban
        :return: if the user was successfully banned
        """
        pass

    @abc.abstractmethod
    def send_mute_req(self, user_id: str, reason: str = None) -> bool:
        """
        sends a request to the server to mute the user

        :param user_id: the user_id to mute
        :param reason: reason for mute
        :return: if the user was successfully muted
        """
        pass
