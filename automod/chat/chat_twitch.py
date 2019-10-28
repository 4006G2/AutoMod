from . import ChatBase
import twitch


class ChatTwitch(ChatBase):

    def __init__(self, chat_bot, token):
        super().__init__(chat_bot)
        self.bot = token
        self.client = twitch.Helix

