import discord
from discord.ext import commands
import unicodedata
import re
from colorama import Fore

class NicknameChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_default_font(self, username):
        # Check if all characters are in the default Unicode range for basic Latin alphabet
        for char in username:
            if unicodedata.category(char)[0] != 'L' and not char.isdigit() and char not in ' -_':
                return False
        return True

    def is_english(self, username):
        # Check if the username contains only English letters and common punctuation
        return re.match(r'^[A-Za-z0-9 _\-]+$', username) is not None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not self.is_default_font(member.name) or not self.is_english(member.name):
            channel = self.bot.get_channel(1268748482592899145)
            default_nickname = f"[Change Nickname]"
            await member.edit(nick=default_nickname)
            await channel.send(f"Your nickname has been changed to {default_nickname} because your username contains non-English or non-standard characters.")
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after, member):
        if before.nick != after.nick:
            if not self.is_default_font(after.name) or not self.is_english(after.name):
                channel = self.bot.get_channel(1269607515952382002)
                default_nickname = f"[Change Nickname]"
                await member.edit(nick=default_nickname)
                await channel.send(f"Your nickname has been changed to {default_nickname} because your username contains non-English or non-standard characters.")

            

async def setup(bot):
    await bot.add_cog(NicknameChecker(bot))
