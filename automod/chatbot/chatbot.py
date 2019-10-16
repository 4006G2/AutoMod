__author__ = "Benedict Thompson"
__version__ = "0.1p"

import re
from typing import Union, List, Pattern

import automod.chat as chat
import automod.game_api as game


class ChatBot(object):
    name: str = "AutoMod"
    greetings: List[str] = ["Hi", "Hello", "Hey"]
    regex_greeting: str = "({0})(?:,? {1})?".format('|'.join(greetings), name)
    pattern_greeting: Pattern = re.compile(regex_greeting)

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
        reply = None
        if message.startswith('!'):
            reply = self.parse_command(message)
        else:
            reply = self.parse_message(message)
        if reply is not None:
            self.server.send_message_to(user_id, reply)

    def parse_message(self, message: str) -> Union[str, None]:
        match = self.pattern_greeting.match(message)
        if match is not None:
            return "Hi"

        return None

    def parse_command(self, message: str) -> Union[str, None]:
        regex_command = r"!(\w+)((?: \w+:\w+)+)?"
        pattern_command = re.compile(regex_command)

        match = pattern_command.match(message)
        if match is not None:
            command = match.group(1)
            params = match.group(2)
            if params is not None:
                params = params.split()
                kwargs = {}
                for p in params:
                    p = p.split(':')
                    kwargs[p[0]] = p[1]
                return self.game_api.send(command, **kwargs)
            else:
                return self.game_api.send(command)
        return None
