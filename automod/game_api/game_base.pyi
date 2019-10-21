__author__ = "Benedict Thompson"
__version__ = "0.1p"

import abc


class GameBase(abc.ABC):
    @property
    @abc.abstractmethod
    def commands(self) -> str:
        ...

    @abc.abstractmethod
    def send(self, command: str, **properties) -> str:
        ...

    @property
    @abc.abstractmethod
    def name(self) -> str:
        ...
