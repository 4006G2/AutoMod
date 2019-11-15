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

    # def test_raise(self):
    #     dt = [0, 25, 10, 30, 15, 5, 26, 24, -10]
    #     for _t in dt:
    #         t = time.time() - _t
    #         with self.subTest(t=_t):
    #             ret = self.chat_bot.raise_discussion(t)
    #             if _t < 25:
    #                 self.assertIsNone(ret)
    #             else:
    #                 self.assertIsNotNone(ret)


if __name__ == '__main__':
    unittest.main()
