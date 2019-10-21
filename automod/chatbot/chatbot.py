__author__ = "Benedict Thompson"
__version__ = "0.1p"

import random
import re
from enum import Enum

import requests


class MessageTone(Enum):
    POSITIVE = 1
    NEUTRAL = 0
    NEGATIVE = -1


class WarningLevel(Enum):
    WARNING = 0
    MUTE = 1
    BAN = 2


class ChatBot(object):
    name = "AutoMod"
    greetings = ["Hi", "Hello", "Hey"]
    regex_greeting = "({0})(?:,? {1})?".format('|'.join(greetings), name)
    pattern_greeting = re.compile(regex_greeting)

    def __init__(self):
        super().__init__()
        self._watch_list = {}
        self._server = None
        self._game = None

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, value):
        self._server = value

    @property
    def game_api(self):
        return self._game

    @game_api.setter
    def game_api(self, value):
        self._game = value

    def on_message(self, user_id, message):
        if message.startswith('!'):
            reply = self.parse_command(message)
        else:
            reply = self.parse_message(message)

        return reply

    def parse_message(self, message):
        match = self.pattern_greeting.match(message)
        if match is not None:
            return random.choice(self.greetings)

        return None

    def parse_command(self, message):
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

    @staticmethod
    def get_behaviour(message):
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

    def monitor_behaviour(self, user_id, message):
        """
        :param user_id: user who sent the message
        :param message: whole text entered by the user
        :return: Enum value of the level of warning of the user
        """
        #  we don't care about them if they haven't been reported.
        if user_id not in self._watch_list:
            return None

        tone = self.get_behaviour(message)
        strikes = 'strikes'
        level = 'level'
        if tone == MessageTone.NEGATIVE:
            self._watch_list[user_id][strikes] += 1
        elif tone == MessageTone.POSITIVE:
            self._watch_list[user_id][strikes] -= 0.2

        if self._watch_list[user_id][strikes] >= 3:
            if self._watch_list[user_id][level] is None:
                # self.warn_user(user)
                self._watch_list[user_id][level] = WarningLevel.WARNING
                self._watch_list[user_id][strikes] -= 3
                return WarningLevel.WARNING
            elif self._watch_list[user_id][level] == WarningLevel.WARNING:
                # self.mute_user(user)
                self._watch_list[user_id][level] = WarningLevel.MUTE
                self._watch_list[user_id][strikes] -= 1
                return WarningLevel.MUTE
            else:
                # self.ban_user(user)
                self._watch_list[user_id][level] = WarningLevel.BAN
                return WarningLevel.BAN
        return None
