__author__ = "Benedict Thompson"
__version__ = "0.1p"

import abc


class ChatBase(abc.ABC):
    def __init__(self, chat_bot):
        super().__init__()
        self.chat_bot = chat_bot
        chat_bot.server = self

    @abc.abstractmethod
    def broadcast_message(self, ch_name, message):
        pass

    @abc.abstractmethod
    def send_message_to(self, user_id, message):
        pass

    @abc.abstractmethod
    def send_ban_req(self, user_id, reason=None):
        pass

    @abc.abstractmethod
    def send_mute_req(self, user_id, reason=None):
        """
        sends a request to the server to mute the user
        :param user_id: the user_id to mute
        :param reason: reason for mute
        :return: if the user was successfully muted
        """
        pass
