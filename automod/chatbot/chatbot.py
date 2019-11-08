__author__ = "Benedict Thompson"
__version__ = "0.1p"

import random
import re
import time
from enum import Enum
import os

import csv
import requests

import time
import datetime


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
    events = []

    def __init__(self):
        super().__init__()
        self._watch_list = {}
        self._server = None
        self._game = None
        self.events = []  # [(time, event), ...]
        self.register_events()
        self._discussion_points = []
        self.init_discussion()
        self.user_msg = {}

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

    def report_user(self, user_id):
        self._watch_list[user_id] = {'strikes': 0, 'level': None}

    def monitor_behaviour(self, user_id, message):
        """
        :param user_id: user who sent the message
        :param message: whole text entered by the user
        :return: Enum value of the level of warning of the user
        """
        #  we don't care about them if they haven't been reported.
        if user_id not in self._watch_list:
            return -1
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
                return WarningLevel.WARNING.value
            elif self._watch_list[user_id][level] == WarningLevel.WARNING:
                # self.mute_user(user)
                self._watch_list[user_id][level] = WarningLevel.MUTE
                self._watch_list[user_id][strikes] -= 1
                return WarningLevel.MUTE.value
            else:
                # self.ban_user(user)
                self._watch_list[user_id][level] = WarningLevel.BAN
                return WarningLevel.BAN.value
        return -1

    # this function should read a text file containing the stream events and the time of it happening
    def register_events(self):
        """
        :rtype: None
        """
        file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'events.txt')
        with open(file) as csvfile:
            data = csv.reader(csvfile)
            for row in data:
                time_in = row[0]
                split_time = time_in.split(':')
                hours = int(split_time[0])
                minutes = int(split_time[1])
                today = datetime.date.today()
                time_today = datetime.datetime(today.year, today.month, today.day, hours, minutes)
                self.events.append((time_today, row[1]))
            # self.events = [(e[0], e[1]) for e in data]
            self.events.sort(key=lambda t: t[0])

    # this function should check the system time and alert chat when an event is happening in
    # 1 hour, 30 mins, 15 mins and 5 mins
    def event_alert(self):
        """
        :rtype: str
        """
        # if current time > event time - 1 hour, 30 mins, 15 mins or 5 mins --> alert chat
        cur_time = datetime.datetime.today()
        alert = ''
        if self.find_alert_time(self.events[0][0], 5) <= cur_time < self.events[0][0]:
            alert = f"{self.events[0][1]} is happening in 5 minutes!"
            self.events.pop(0)
        elif self.find_alert_time(self.events[0][0], 15) <= cur_time < self.events[0][0]:
            alert = f"{self.events[0][1]} is happening in 15 minutes!"
        elif self.find_alert_time(self.events[0][0], 30) <= cur_time < self.events[0][0]:
            alert = f"{self.events[0][1]} is happening in 30 minutes!"
        elif self.find_alert_time(self.events[0][0], 60) <= cur_time < self.events[0][0]:
            alert = f"{self.events[0][1]} is happening in 1 hour!"
        return alert

    def find_alert_time(self, e_time, t):
        if t == 60:
            return datetime.datetime(e_time.year, e_time.month, e_time.day, e_time.hour - 1, e_time.minute)
        else:
            if (e_time.minute - t) < 0:
                return datetime.datetime(e_time.year, e_time.month, e_time.day, e_time.hour - 1,
                                         e_time.minute + 60 - t)
            else:
                return datetime.datetime(e_time.year, e_time.month, e_time.day, e_time.hour, e_time.minute - t)

    def init_discussion(self):
        file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'info.txt')
        with open(file, 'r') as read_info:
            self._discussion_points = read_info.readlines()

    def raise_discussion(self, last_message):
        """
        Checks how much time has passed since the last message, and returns something to say if it has been too long
        :param last_message the time of the last message (epoch seconds)
        :return: a string to print or None
        *Note: this function should be called with a variable assigned with the starting point before when an input is met
        """
        downtime = time.time() - last_message.created_at.timestamp()
        sender = str(last_message.author)
        sender_name = sender.split('#')[0]

        if sender_name == "ModeratorBot" or downtime < 25:
            return ''
        else:
            return random.choice(self._discussion_points)

    def is_spam(self, user, msg_t, message):
        spam = False
        if user not in self.user_msg:  # check if user exists in dict
            self.user_msg[user] = []
        elif len(self.user_msg[user]) == 5:  # check if user has 5 messages saved
            self.user_msg[user].pop(0)
        self.user_msg[user].append((msg_t, message))
        if len(self.user_msg[user]) >= 3:  # similarity check
            if self.same_msg(self.user_msg[user]):
                spam = True
        if len(self.user_msg[user]) == 5:  # too many msg too soon
            if self.too_many_msg(self.user_msg[user]):
                spam = True
        return spam

    def same_msg(self, msg_lst):
        same = False
        for i in range(len(msg_lst)-1):
            if msg_lst[i][1] == msg_lst[i+1][1]:
                same = True
            else:
                return False
        return same

    def too_many_msg(self, msg_lst):
        t_interval = msg_lst[0][0] - msg_lst[len(msg_lst)-1][0]
        if t_interval.seconds >= 10:
            return True
        else:
            return False

# testing
# if __name__ == "__main__":
#     import datetime
#     cb = ChatBot()
#     usr = 'user'
#     msg1 = 'hi'
#     msg1_t = datetime.datetime(2019, 11, 2, 17, 5, 22)
#     msg2 = 'hello'
#     msg2_t = datetime.datetime(2019, 11, 2, 17, 5, 23)
#     msg3 = 'no'
#     msg3_t = datetime.datetime(2019, 11, 2, 17, 5, 24)
#     msg4 = 'way'
#     msg4_t = datetime.datetime(2019, 11, 2, 17, 5, 25)
#     msg5 = 'yes'
#     msg5_t = datetime.datetime(2019, 11, 2, 17, 5, 31)
#     msg6 = 'me'
#     msg6_t = datetime.datetime(2019, 11, 2, 17, 5, 32)
#     cb.is_spam(usr, msg1_t, msg1)
#     print(cb.user_msg)
#     cb.is_spam(usr, msg2_t, msg2)
#     print(cb.user_msg)
#     cb.is_spam(usr, msg3_t, msg3)
#     print(cb.user_msg)
#     cb.is_spam(usr, msg4_t, msg4)
#     print(cb.user_msg)
#     cb.is_spam(usr, msg5_t, msg5)
#     print(cb.user_msg)
#     cb.is_spam(usr, msg6_t, msg6)
#     print(cb.user_msg)
#
#
# if __name__ == "__main__":
#     c = ChatBot()
#     c.register_events()
#     c.event_alert()
#     c.event_alert()
#
#
# if __name__ == "__main__":
#     c = ChatBot()
#     message = "Hi"
#     print(c.get_behaviour(message))
#     message = "very bad"
#     print(c.get_behaviour(message))
#     message = "very good"
#     print(c.get_behaviour(message))
