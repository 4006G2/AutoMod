__author__ = "Benedict Thompson"
__version__ = "0.1p"

import unittest
from typing import Dict

from .chatbot import ChatBot, MessageTone

POSITIVE = MessageTone.POSITIVE
NEUTRAL = MessageTone.NEUTRAL
NEGATIVE = MessageTone.NEGATIVE


class ChatBotTests(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.chat_bot = ChatBot()

    def test_user_language(self):
        test_data: Dict[str, MessageTone] = {}

        for message, expected in test_data:
            with self.subTest(message=message):
                self.assertEqual(self.chat_bot.get_behaviour(message), expected)

    def test_func(self):
        message = input("")
        m = self.chat_bot.raise_discussion()
        self.assertTrue(m)
        self.assertFalse(m)

if __name__ == '__main__':
    unittest.main()
