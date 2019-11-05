from . import ChatBase
import discord
import asyncio


class ChatDiscord(ChatBase):
    def __init__(self, chat_bot, token):
        super().__init__(chat_bot)
        self.token = token
        self.client = discord.Client()
        self.client.event(self.on_message)
        self.guilds = self.client.guilds

    async def find_guild_id(self, guild_name):
        guilds = await self.client.fetch_guilds(limit=10).flatten()
        for guild in guilds:
            if guild.name == guild_name:
                return guild.id
        return None

    def find_channel_id(self, ch_name):
        for ch in self.client.get_all_channels():
            if ch.name == ch_name:
                return ch.id
        return None

    def find_user_id(self, user_name):
        for user in self.client.get_all_members():
            if user.name == user_name:
                return user.id
        return None

    async def get_last_msg(self, ch_name):
        ch_id = self.find_channel_id(ch_name)
        ch = self.client.get_channel(ch_id)
        async for message in ch.history(limit=1):
            return message

    async def send_message_to_id(self, user_id, message):
        user = self.client.get_user(user_id)
        await user.send(message)

    async def broadcast_message(self, ch_name, message):
        ch_id = self.find_channel_id(ch_name)
        ch = self.client.get_channel(ch_id)
        await ch.send(message)
        await self.client.close()

    async def send_message_to(self, user_name, message):
        user_id = self.find_user_id(user_name)
        user = self.client.get_user(user_id)
        await user.send(message)

    async def send_ban_req(self, user_name, reason=None):
        user_id = self.find_user_id(user_name)
        user = self.client.get_user(user_id)
        guild_id = self.find_guild_id('AutoModTesting')
        guild = self.client.get_guild(guild_id)
        if reason is None:
            reason = "You are unworthy."
        message = f"{user_name} have been banned for {reason}!"
        await guild.ban(user, reason=reason)
        await self.broadcast_message('general', message)
        await self.client.close()

    async def find_banned_user(self, user_name):
        guild_id = self.find_guild_id('AutoModTesting')
        guild = self.client.get_guild(guild_id)
        banned = await guild.bans()
        for (reason, user) in banned:
            if user.name == user_name:
                return user
        return None

    async def print_banned(self):
        guild_id = self.find_guild_id('AutoModTesting')
        guild = self.client.get_guild(guild_id)
        banned = await guild.bans()
        for (reason, user) in banned:
            print(reason, user)
        await self.client.close()

    async def unban(self, user_name, reason=None):
        user = await self.find_banned_user(user_name)
        guild_id = self.find_guild_id('AutoModTesting')
        guild = self.client.get_guild(guild_id)
        message = f"{user_name} have been unbanned for {reason}!"
        await guild.unban(user)
        await self.broadcast_message('general', message)
        await self.client.close()

    async def send_mute_req(self, user_name, ch_name, reason=None):
        user_id = self.find_user_id(user_name)
        user = self.client.get_user(user_id)
        ch_id = self.find_channel_id(ch_name)
        ch = self.client.get_channel(ch_id)
        if reason is None:
            reason = "Cause I can."
        message = f"{user_name} have been muted for {reason}!"
        await ch.set_permissions(user, read_messages=True, send_messages=False)
        await self.broadcast_message('general', message)
        await self.client.close()

    async def unmute(self, user_name, ch_name, reason=None):
        user_id = self.find_user_id(user_name)
        user = self.client.get_user(user_id)
        ch_id = self.find_channel_id(ch_name)
        ch = self.client.get_channel(ch_id)
        message = f"{user_name} have been unmuted for {reason}!"
        await ch.set_permissions(user, overwrite=None)
        await self.broadcast_message('general', message)
        await self.client.close()

    # client.event
    async def on_message(self, message):
        user_id = message.author.id
        username = message.author.split('#')[0]
        if user_id != self.find_user_id('ModeratorBot'):  # check if sender is the bot
            if self.chat_bot.is_spam(user_id, message.time, message.content):  # spam check
                self.send_mute_req(username, "Spamming")
            if user_id not in self.chat_bot.watch_list:  # check if sender is monitored
                action = await self.chat_bot.monitor_behaviour(user_id, message)
                if action == 0:
                    self.send_message_to(username, 'Please stop sending toxic messages!')
                elif action == 1:
                    self.send_mute_req(username, "Toxic behaviour.")
                elif action == 2:
                    self.send_ban_req(username, "Toxic behaviour.")

    async def tasks(self):
        await self.client.wait_until_ready()
        while not self.client.is_closed():
            last_msg = await self.get_last_msg('general')
            prompt = await self.chat_bot.raise_discussion(last_msg.created_at.timestamp())
            if len(prompt) != 0:
                self.broadcast_message('general', prompt)
            alert = await self.chat_bot.event_alert()
            if len(alert) != 0:
                self.broadcast_message('general', alert)
            await asyncio.sleep(60)
