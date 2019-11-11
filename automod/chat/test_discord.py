import unittest
from . import ChatDiscord
from automod.chatbot import ChatBot
import json

with open('keys.json') as keys:
    key_dict = json.loads(keys.read())
    TOKEN = key_dict['discord']


class DiscordTests(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.cb = ChatBot()
        self.test_server = ChatDiscord(self.cb, TOKEN)

    def test(self):
        srvr = self.test_server.client


if __name__ == '__main__':
    unittest.main()
