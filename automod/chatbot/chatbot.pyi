from enum import Enum
from typing import Pattern, List, Dict, Union, Optional

from automod.chat import ChatBase
from automod.game_api import GameBase


class MessageTone(Enum):
    POSITIVE = 1
    NEUTRAL = 0
    NEGATIVE = -1


class WarningLevel(Enum):
    WARNING = 0
    MUTE = 1
    BAN = 2


class ChatBot(object):
    name: str = ...
    greetings: List[str] = ...
    regex_greeting: str = ...
    pattern_greeting: Pattern = ...

    def __init__(self) -> None:
        self._discussion_points: List[str] = ...
        self._watch_list: Dict[str, Dict[str, Union[float, WarningLevel]]] = ...
        self._game: GameBase = ...
        self._server: ChatBase = ...
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

    @staticmethod
    def get_behaviour(message: str) -> MessageTone:
        ...

    def monitor_behaviour(self, user_id: str, message: str):
        ...

    def init_discussion(self) -> None:

    def raise_discussion(self, t_message: int) -> Optional[str]:
        ...
