
import discord
import asyncio
from discord.ext import commands
import os
from dotenv import load_dotenv, dotenv_values
from discord.ext.commands import is_owner

import sys


import sys
project_root = 'C:\\Users\\Vinea\\Desktop\\Personal Projects\\ybot'
sys.path.append(project_root)



load_dotenv()
TOKEN = os.getenv("BOT_SECRET_TOKEN")
PREFIX = "!"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, status=discord.Status.idle, activity=discord.Game(name="Bot Activities"), application_id="1027772366476017677")
@bot.event   
async def on_ready():
    print("bot is ready!")
    print(bot.user)

@bot.event
async def on_message_delete(message):
    memb = message.author
    
    channel = bot.get_channel(1130593170053398581)
    mlog = f"Message sent by <@{memb.id}> deleted in <#{message.channel.id}>\n**Contents:** {message.content}"
    embed = discord.Embed(description = mlog, color = discord.Colour.random())
    embed.set_author(name=memb.name,icon_url=message.author.avatar)
    await channel.send(embed=embed)

@bot.event           
async def on_message(message: discord.Message):
    await bot.process_commands(message)
    if message in bot.tree.get_commands():
        print("Valid command")

@bot.command()
@is_owner()
async def shutdown(ctx):
    await bot.application.owner.send(content=f"Bot shutting down...\nShut down command initialized by {ctx.author.name}")
    await bot.close()

@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

@bot.command()
@is_owner()
async def sync(ctx):
    await ctx.bot.tree.sync()
    await ctx.send("Commands are synced!")

async def load():
    for file in os.listdir(os.path.join(project_root, 'src', 'cogs')):
        if file.endswith('.py'):
            await bot.load_extension(f'src.cogs.{file[:-3]}')
async def main():
    await load()
    await bot.start(TOKEN)
asyncio.run(main())