import discord
from discord.ext import commands
import unicodedata
import re
import time

class NicknameChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_update = {}  # Store the last time a nickname change was processed

    def is_default_font(self, username):
        for char in username:
            if unicodedata.category(char)[0] != 'L' and not char.isdigit() and char not in ' -_':
                return False
        return True

    def is_english(self, username):
        return re.match(r'^[A-Za-z0-9 _\-]+$', username) is not None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not self.is_default_font(member.name) or not self.is_english(member.name):
            channel = self.bot.get_channel(1268748482592899145)
            default_nickname = "[Change Nickname]"
            await member.edit(nick=default_nickname)
            await channel.send(f"Your nickname has been changed to {default_nickname} because your username contains non-English or non-standard characters.")

# Please fix
"""
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            # Prevent multiple messages for the same change
            current_time = time.time()
            if after.id in self.last_update and (current_time - self.last_update[after.id]) < 60:
                return

            if not self.is_default_font(after.name) or not self.is_english(after.name):
                channel = self.bot.get_channel(1269607515952382002)
                default_nickname = "[Change Nickname]"
                try:
                    await after.edit(nick=default_nickname)
                    await channel.send(f"{after.mention}, your nickname has been changed to {default_nickname} because your username contains non-English or non-standard characters.")
                    self.last_update[after.id] = current_time  # Update the last change time
                except Exception as e:
                    await channel.send(f"Failed to change nickname for {after.mention}. Error: {e}")
"""

async def setup(bot):
    await bot.add_cog(NicknameChecker(bot))
