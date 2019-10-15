__author__ = "Benedict Thompson"
__version__ = "0.1p"

import abc


class ChatBase(abc.ABC):
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
