__author__ = "Benedict Thompson"
__version__ = "0.1p"

import abc


class GameBase(abc.ABC):
    @property
    @abc.abstractmethod
    def commands(self):
        """
        get the commands allowed by the game API

        :return: a dict containing the commands and a dictionary of the allowed kw args and if they are required
        """
        pass

    @abc.abstractmethod
    def send(self, command, **properties):
        """
        Sends a request to the game's API based on the passed command

        :param command: the command/info required
        :param properties: the properties to accompany the request
        :return: the information returned by the API
        """
        pass

    @property
    @abc.abstractmethod
    def name(self):
        """
        :return: the name for the game/api
        """
        pass
