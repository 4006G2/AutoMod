from . import ChatBase
import discord


class ChatDiscord(ChatBase):
    def __init__(self, chat_bot, token):
        super().__init__(chat_bot)
        self.bot = token
        self.client = discord.Client()

    def find_user_id(self, user_name):
        for user in self.client.get_all_members():
            if user.name == user_name:
                return user.id
        return None

    async def broadcast_message(self, message, channel_id) -> None:
        ch = self.client.get_channel(channel_id)
        await ch.send(message)
        await self.client.close()

    async def send_message_to(self, user_name, message) -> None:
        user_id = self.find_user_id(user_name)
        user = self.client.get_user(user_id)
        await user.send(message)

    def send_ban_req(self, user_id, reason=None) -> bool:
        pass  # TODO

    def send_mute_req(self, user_id: str, reason=None) -> bool:
        pass  # TODO
