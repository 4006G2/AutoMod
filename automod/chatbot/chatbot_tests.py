__author__ = "Benedict Thompson"
__version__ = "0.1p"

import unittest

from .chatbot import ChatBot


class ChatBotTests(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.chat_bot = ChatBot()

    def test_func(self):
        message = input("")
        m = self.chat_bot.raise_discussion()
        self.assertTrue(m)
        self.assertFalse(m)

if __name__ == '__main__':
    unittest.main()
