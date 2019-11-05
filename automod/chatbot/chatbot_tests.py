__author__ = "Benedict Thompson"
__version__ = "0.1p"

import unittest

from .chatbot import ChatBot, MessageTone
import timeit

POSITIVE = MessageTone.POSITIVE
NEUTRAL = MessageTone.NEUTRAL
NEGATIVE = MessageTone.NEGATIVE


class ChatBotTests(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.chat_bot = ChatBot()

    def test_user_language(self):
        test_data = {"Hi": NEUTRAL, "very bad": NEGATIVE, "very good": POSITIVE}

        for message, expected in test_data.items():
            with self.subTest(message=message):
                self.assertEqual(self.chat_bot.get_behaviour(message), expected)

    def test_raise(self):
        t_message = timeit.default_timer()
        msg = input()
        m = self.chat_bot.raise_discussion(t_message)
        self.assertTrue(m)


if __name__ == '__main__':
    unittest.main()
