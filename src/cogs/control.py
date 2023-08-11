import discord
from discord.ext import commands
from discord import app_commands
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\.."))
print(f"PR Control: {project_root}")
sys.path.append(project_root)

from src.utils.utility import Utility

class BotControl(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("control cog loaded!")

    @commands.command(brief="syncs commands", description="this command helps sync bot commands across guilds")
    @commands.is_owner()
    async def sync(self, ctx):
        print("is owner confirmed")
        try:
            await self.bot.tree.sync()
            print("tree synced")
            await ctx.send("Commands are synced!")
        except Exception as e:
            print("Error during sync:", e)
            await ctx.send("An error occurred during sync.")

    @commands.command(name= "shutdown", brief="shuts down bot")
    @commands.is_owner()
    async def shutdown(self, ctx):
        await self.bot.application.owner.send(content=f"Bot shutting down...\nShut down command initialized by {ctx.author.name}")
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(BotControl(bot))
    
    