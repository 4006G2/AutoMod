__author__ = "Benedict Thompson"
__version__ = "0.1p"

import random
import re


class ChatBot(object):
    name = "AutoMod"
    greetings = ["Hi", "Hello", "Hey"]
    regex_greeting = "({0})(?:,? {1})?".format('|'.join(greetings), name)
    pattern_greeting = re.compile(regex_greeting)

    def __init__(self):
        super().__init__()
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
