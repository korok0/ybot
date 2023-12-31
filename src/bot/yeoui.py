import discord
import asyncio
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord.ext.commands import is_owner
import sys

project_root = os.getcwd()
print(f"PR Yeoui: {project_root}")
sys.path.append(project_root)

load_dotenv()
TOKEN = os.getenv("BOT_SECRET_TOKEN")
APPLICATION_ID = os.getenv("BOT_APPLICATION_ID")

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all(), status=discord.Status.online, activity=discord.Game(name="Bot Activities"), application_id=APPLICATION_ID)
     
    async def on_ready(self):
        print(f"{self.user} is ready!")
    
    async def load(self):
        for file in os.listdir(os.path.join(project_root, "src\\cogs\\")):
            if file.endswith('.py'):
                await self.load_extension(f'src.cogs.{file[:-3]}')

async def main():
    bot = Bot()
    await bot.load()
    await bot.start(TOKEN)
asyncio.run(main())