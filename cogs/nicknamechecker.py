import discord
from discord.ext import commands
import unicodedata
import re

class NicknameChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_nickname = {}  # Track last nickname to prevent multiple messages
        self.ignore_updates = set()  # To track bot's own updates

    def is_default_font(self, text):
        """
        Check if the text uses only default font characters (letters, digits, spaces, hyphens, and underscores).
        """
        for char in text:
            if unicodedata.category(char)[0] not in ('L', 'N') and char not in ' -_':
                return False
        return True

    def is_english(self, text):
        """
        Check if the text contains only English letters, digits, spaces, hyphens, and underscores.
        """
        return bool(re.match(r'^[A-Za-z0-9 _\-]+$', text))

    async def notify_user(self, member, message):
        """
        Send a notification message to the user in a specific channel.
        """
        channel = self.bot.get_channel(1270692641633210378)
        if channel is None:
            print("Error: Notification channel not found.")
            return

        try:
            await channel.send(f"{member.mention}: {message}")
        except discord.DiscordException as e:
            print(f"Failed to send message to channel {channel.id}: {e}")

    async def handle_nickname_change(self, member, new_nickname):
        """
        Handle the process of changing a member's nickname and sending a notification.
        """
        # Check if the new nickname is valid
        if not self.is_default_font(new_nickname) or not self.is_english(new_nickname):
            default_nickname = "[Change Nickname]"
            try:
                self.ignore_updates.add(member.id)
                await member.edit(nick=default_nickname)
                await self.notify_user(member, f"Your nickname has been changed to {default_nickname} due to non-standard characters.")
                # Update the last nickname
                self.last_nickname[member.id] = default_nickname
            except discord.DiscordException as e:
                print(f"Failed to change nickname for {member.id}: {e}")
            finally:
                self.ignore_updates.discard(member.id)
        else:
            # Update the last nickname to the valid one
            self.last_nickname[member.id] = new_nickname

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Handle new members joining the server.
        """
        await self.handle_nickname_change(member, member.name)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """
        Handle changes to a member's nickname.
        """
        if after.id in self.ignore_updates:
            # Ignore updates made by the bot itself
            return

        if after.nick and after.nick != before.nick:
            if after.id not in self.last_nickname or self.last_nickname[after.id] != after.nick:
                await self.handle_nickname_change(after, after.nick)

async def setup(bot):
    await bot.add_cog(NicknameChecker(bot))
