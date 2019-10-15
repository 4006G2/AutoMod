import unittest

from .chatbot import ChatBot


class MyTestCase(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.chat_bot = ChatBot()


if __name__ == '__main__':
    unittest.main()
