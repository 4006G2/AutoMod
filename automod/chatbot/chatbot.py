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
    users = \
        [
            "Akeanused",
            "Alogeene",
            "AnimationScan",
            "Aphorks",
            "BasePlay",
            "Beatterso",
            "BotCartoons",
            "Boutiquest",
            "Bulletiner",
            "Cacheeletow",
            "CamHeadline",
            "CartoonsGames",
            "Cegettele",
            "ClassTailored",
            "Cleohmen",
            "Cloudydom",
            "ComboPlatform",
            "ComediesFocus",
            "Comperco",
            "CornerDeep",
            "Corpoist",
            "Corriflex",
            "CubeStory",
            "Deerfoo",
            "Dingbitu",
            "DirectSpot",
            "Dramalianso",
            "DramasData",
            "Dynewood",
            "Edntrani",
            "EnterBonus",
            "EnterLevel",
            "Exclusive",
            "Favoritera",
            "Featuredbb",
            "Fluxbrya",
            "FragArea",
            "Franceli",
            "Gendschn",
            "Gostrysc",
            "InfoEngine",
            "Koryseed",
            "Leaguester",
            "Ledarts",
            "Lensacifoc",
            "Locallicser",
            "Lyngsead",
            "Mediainte",
            "Mentecon",
            "MessagesAction",
            "Mixtufaul",
            "MonoArea",
            "MultiplayerPlayer",
            "Networket",
            "NewsTactics",
            "Praxisli",
            "ProductionsEpic",
            "Prosence",
            "Proverla",
            "Pulebanc",
            "Radiusefiy",
            "Razorac",
            "ReplaySpot",
            "Reportsca",
            "Screencely",
            "ScreenMachine",
        ]

    talkingPoints = \
        [
            "For more updates from the streamer, hit the follow and subsribe button",
            "*Warning* For any offend towards other users you can get mute or ban",
            "Event on: Nov 2019, 14th, ESI Autumn Forum, London",
            "Don't miss: Nov 2019, 15-17th, DreamHack Atlanta, Georgia, USA",
            "Be on: Dec 2019, 3-4th, Everything in Sport: Women Edition, London, UK",
            "Next on Esports - LoL World Championship: Griffing vs Invictus Gaming - Sat 26 Oct, 1:00 PM",
            "LoL World Championship: FunPlus Phoneix vs Fnatic - Sat 26 Oct, 6 PM",
            "LoL World Championship: SK Telecom T1 vs Splyce - Sun 27 Oct 1 PM",
            "LoL World Championship: DAMWON Gaming vs G2 - Sun 27 Oct 6 PM"
        ]

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

    # this function should detect if the user gives no input, then print out some talking points
    def raise_discussion(self, msg: str):
        """
        -Check if any function with input does not receive input
        -if it does not receive, print: some talking points or future events
        :type msg: object
        :rtype: None

        """

        print("You have entered in the stream chatroom")

        while True:
            rand_tk = random.randint(0, len(self.talkingPoints))
            rand_subs = random.randint(1, 12)
            rand_time = float(random.uniform(1.5, 5))
            rand_user = random.randint(0, len(self.users))
            rand_donation = float(random.uniform(1.23, 20.67))

            # Here should check if the main functions with input
            message = msg

            if message == ""
                time.sleep(rand_time)
                print(self.talkingPoints[rand_tk - 1])
            elif message == "/quit":
                print("You have exited the chatroom")
                break
            else:

                time.sleep(rand_time)
                # users that entered in the chatroom
                print(str(rand_subs) + " users entered in the chatroom")
                time.sleep(rand_time + 8)
                # donations
                print("The user '" + str(self.users[rand_user - 1]) + "' has donated " + str(round(rand_donation, 2)) + " £")
         return None
