import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore
import asyncio
import os

class BanNoPfpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{Fore.GREEN}[ OK ]{Fore.RESET} ban_pfp.py")
        print(f'Logged in as {self.bot.user.name} ({self.bot.user.id})')
        guild = self.bot.guilds[0]  # Assumes the bot is in only one server, adjust if needed
        banned_users = []

        for member in guild.members:
            if member.bot:
                continue
            if member.avatar is None:
                try:
                    await member.ban(reason="No profile picture")
                    banned_users.append(member)
                    print(f"Banned {member.name}#{member.discriminator}")
                except Exception as e:
                    print(f"Failed to ban {member.name}#{member.discriminator}: {e}")

        if banned_users:
            channel = self.bot.get_channel(1270579451398459402)
            banned_list = "\n".join([f"{user.id}" for user in banned_users])
            await channel.send(f"Banned the following users for not having a profile picture:\n{banned_list}")
        else:
            print("No users without profile pictures found.")

        await self.bot.close()

def setup(bot):
    bot.add_cog(BanNoPfpCog(bot))
