__author__ = "Benedict Thompson"
__version__ = "0.1p"

import re
from enum import Enum
from typing import Union, List, Pattern, Dict

import requests

import automod.chat as chat
import automod.game_api as game


class MessageTone(Enum):
    POSITIVE = 1
    NEUTRAL = 0
    NEGATIVE = -1


class WarningLevel(Enum):
    WARNING = 0
    MUTE = 1
    BAN = 2


class ChatBot(object):
    name: str = "AutoMod"
    greetings: List[str] = ["Hi", "Hello", "Hey"]
    regex_greeting: str = "({0})(?:,? {1})?".format('|'.join(greetings), name)
    pattern_greeting: Pattern = re.compile(regex_greeting)

    def __init__(self) -> None:
        super().__init__()
        self._server: Union[chat.ChatBase, None] = None
        self._game: Union[game.GameBase, None] = None
        self._watch_list: Dict[str, Dict] = dict()

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

    def get_behaviour(self, message: str) -> MessageTone:
        """
        :param message: user input
        :return: Enum value of negative, neutral, positive
        """

        # sends HTTP POST request to NLP Sentiment detection API.
        # response in JSON of:
        # {
        #   'probability': {
        #       'neg': 0.3272625669931226,
        #       'neutral': 0.416401965581632,
        #       'pos': 0.6727374330068774
        #   },
        #   'label': 'pos'
        # }

        req = requests.post(url="http://text-processing.com/api/sentiment/", data="text={0}".format(message))
        response = req.json()
        tone_value = response['label']

        if tone_value == 'neg':
            return MessageTone.NEGATIVE
        elif tone_value == 'pos':
            return MessageTone.POSITIVE
        else:
            return MessageTone.NEUTRAL

    def monitor_behaviour(self, user: str, user_input: str) -> Union[WarningLevel, None]:
        """
        :param user: user who sent the message
        :param user_input: whole text entered by the user
        :return: Enum value of the level of warning of the user
        """
        #  we don't care about them if they haven't been reported.
        if user not in self._watch_list:
            return None

        tone = self.get_behaviour(user_input)
        if tone == MessageTone.NEGATIVE:
            self._watch_list[user][0] += 1
        elif tone == MessageTone.POSITIVE:
            self._watch_list[user][0] -= 0.2

        if self._watch_list[user]['strikes'] >= 3:
            if self._watch_list[user]['level'] is None:
                # self.warn_user(user)
                self._watch_list[user]['level'] = WarningLevel.WARNING
                self._watch_list[user]['strikes'] -= 3
                return WarningLevel.WARNING
            elif self._watch_list[user]['level'] == WarningLevel.WARNING:
                # self.mute_user(user)
                self._watch_list[user]['level'] = WarningLevel.MUTE
                self._watch_list[user]['strikes'] -= 1
                return WarningLevel.MUTE
            else:
                # self.ban_user(user)
                self._watch_list[user][1] = WarningLevel.BAN
                return WarningLevel.BAN
        return None
