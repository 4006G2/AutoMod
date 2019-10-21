__author__ = "Benedict Thompson"
__version__ = "0.1p"

import unittest

from .chatbot import ChatBot


class ChatBotTests(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.chat_bot = ChatBot()


if __name__ == '__main__':
    unittest.main()
