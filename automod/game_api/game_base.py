__author__ = "Benedict Thompson"
__version__ = "0.1p"

import abc
from typing import Dict


class GameBase(abc.ABC):
    @abc.abstractmethod
    @property
    def commands(self) -> Dict[str, Dict[str, bool]]:
        """
        get the commands allowed by the game API

        :return: a dict containing the commands and a dictionary of the allowed kw args and if they are required
        """
        pass

    @abc.abstractmethod
    def send(self, command: str, **properties) -> str:
        """
        Sends a request to the game's API based on the passed command

        :param command: the command/info required
        :param properties: the properties to accompany the request
        :return: the information returned by the API
        """
        pass
