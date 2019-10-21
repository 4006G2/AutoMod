from typing import Pattern

from automod.chat import ChatBase
from automod.game_api import GameBase


class ChatBot(object):
    pattern_greeting: Pattern = None

    def __init__(self) -> None:
        self._game: GameBase = None
        self._server: ChatBase = None
        ...

    @property
    def server(self) -> ChatBase:
        ...

    @server.setter
    def server(self, value: ChatBase) -> None:
        ...

    @property
    def game_api(self) -> GameBase:
        ...

    @game_api.setter
    def game_api(self, value: GameBase) -> None:
        ...

    def on_message(self, user_id: str, message: str) -> str:
        ...

    def parse_message(self, message: str) -> str:
        ...

    def parse_command(self, message: str) -> str:
        ...
