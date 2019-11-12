from . import ChatBase
import discord
import asyncio


class ChatDiscord(ChatBase):
    def __init__(self, chat_bot, token):
        super().__init__(chat_bot)
        self.token = token
        self.client = discord.Client()
        self.client.event(self.on_ready)
        self.client.event(self.on_message)
        self.guilds = []
        self.muted = {}

    async def init_guilds(self):
        guilds = await self.client.fetch_guilds(limit=10).flatten()
        for guild in guilds:
            if guild not in self.guilds:
                self.guilds.append(guild)

    async def find_guild_id(self, guild_name):
        for guild in self.guilds:
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

    async def broadcast_message(self, ch_name, message):
        ch_id = self.find_channel_id(ch_name)
        ch = self.client.get_channel(ch_id)
        await ch.send(message)

    async def send_message_to(self, user_name, message):
        user_id = self.find_user_id(user_name)
        user = self.client.get_user(user_id)
        await user.send(message)

    async def send_message_to_id(self, user_id, message):
        user = self.client.get_user(user_id)
        await user.send(message)

    async def get_last_msg(self, ch_name):
        ch_id = self.find_channel_id(ch_name)
        ch = self.client.get_channel(ch_id)
        async for message in ch.history(limit=1):
            return message

    async def send_ban_req(self, user_name, guild_name, reason=None):
        user_id = self.find_user_id(user_name)
        user = self.client.get_user(user_id)
        guild_id = await self.find_guild_id(guild_name)
        guild = self.client.get_guild(guild_id)
        if reason is None:
            reason = "You are unworthy."
        message = f"{user_name} have been banned for {reason}!"
        await guild.ban(user, reason=reason)
        await self.broadcast_message('general', message)

    async def find_banned_user(self, user_name, guild_name):
        guild_id = await self.find_guild_id(guild_name)
        guild = self.client.get_guild(guild_id)
        banned = await guild.bans()
        for (reason, user) in banned:
            if user.name == user_name:
                return user
        return None

    async def print_banned(self, guild_name):
        guild_id = self.find_guild_id(guild_name)
        guild = self.client.get_guild(guild_id)
        banned = await guild.bans()
        for (reason, user) in banned:
            print(reason, user)

    async def unban(self, user_name, guild_name, reason=None):
        user = await self.find_banned_user(user_name, guild_name)
        guild_id = await self.find_guild_id(guild_name)
        guild = self.client.get_guild(guild_id)
        message = f"{user_name} have been unbanned for {reason}!"
        await guild.unban(user)
        await self.broadcast_message('general', message)

    async def send_mute_req(self, user_name, reason=None):
        user_id = self.find_user_id(user_name)
        user = self.client.get_user(user_id)
        if reason is None:
            reason = "Cause I can."
        message = f"{user_name} have been muted for {reason}!"
        for ch in self.client.get_all_channels():
            await ch.set_permissions(user, read_messages=True, send_messages=False)
        self.muted[user_name] = reason
        await self.broadcast_message('general', message)

    async def unmute(self, user_name):
        user_id = self.find_user_id(user_name)
        user = self.client.get_user(user_id)
        for ch in self.client.get_all_channels():
            await ch.set_permissions(user, overwrite=None)

    async def unmute_all(self, reason=None):
        if len(self.muted) != 0:
            for user in list(self.muted):
                await self.unmute(user)
                self.muted.pop(user, None)
                message = f"{user} have been unmuted for {reason}!"
                await self.broadcast_message('general', message)

    def report_all(self):
        for member in self.client.get_all_members():
            username = str(member).split('#')[0]
            if username != "ModeratorBot":
                user_id = self.find_user_id(username)
                self.chat_bot.report_user(user_id)

    async def discussion_prompt(self):
        last_msg = await self.get_last_msg('general')
        prompt = self.chat_bot.raise_discussion(last_msg)
        if len(prompt) != 0:
            await self.broadcast_message('general', prompt)

    async def event_alert(self):
        alert = self.chat_bot.event_alert()
        if len(alert) != 0:
            await self.broadcast_message('general', alert)

    # client.event
    async def on_ready(self):
        await self.init_guilds()
        await self.broadcast_message('general', 'ModeratorBot is online!')

    # client.event
    async def on_message(self, message):
        user_id = message.author.id
        username = str(message.author).split('#')[0]
        if user_id != self.find_user_id('ModeratorBot'):  # check if sender is the bot
            if self.chat_bot.is_spam(user_id, message.created_at, message.content):  # spam check
                await self.send_mute_req(username, reason="Spamming")
            else:
                action = self.chat_bot.monitor_behaviour(user_id, message.content)  # behaviour check
                if action == 0:
                    await self.send_message_to(username, 'Please stop sending toxic messages!')
                elif action == 1:
                    await self.send_mute_req(username, reason="toxic behaviour")
                elif action == 2:
                    await self.send_ban_req(username, str(message.guild), reason="toxic behaviour")

    async def tasks(self):
        await self.client.wait_until_ready()
        self.report_all()  # for prototype testing
        while not self.client.is_closed():  # main loop
            await self.discussion_prompt()
            await self.event_alert()
            await self.unmute_all(reason='mute expired')
            await asyncio.sleep(60)
