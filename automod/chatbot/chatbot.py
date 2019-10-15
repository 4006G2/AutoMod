__author__ = "Benedict Thompson"
__version__ = "0.1p"

import re
from typing import Union

import automod.chat as chat
import automod.game_api as game


class ChatBot(object):
    name = "AutoMod"
    greetings = ["Hi", "Hello", "Hey"]
    pattern_greeting = "({0})(?:,? {1})".format('|'.join(greetings), name)
    expr_greeting = re.compile(pattern_greeting)

    def __init__(self) -> None:
        super().__init__()
        self._server: Union[chat.ChatBase, None] = None
        self._game: Union[game.GameBase, None] = None

    @property
    def server(self) -> chat.ChatBase:
        return self._server

    @server.setter
    def server(self, srvr: chat.ChatBase):
        self._server = srvr

    @property
    def game_api(self) -> game.GameBase:
        return self._game

    @game_api.setter
    def game_api(self, api: game.GameBase):
        self._game = api

    def on_message(self, user_id: str, message: str):
        reply = self.parse_message(message)
        if reply is not None and self.server is not None:
            self._server.send_message_to(user_id, reply)

    def parse_message(self, message: str) -> Union[str, None]:
        match = self.expr_greeting.search(message)
        if match is not None:
            return "Hi"

        return None
