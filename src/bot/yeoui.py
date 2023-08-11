import discord
import asyncio
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord.ext.commands import is_owner
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\.."))
print(f"PR: {project_root}")
sys.path.append(project_root)

load_dotenv()
TOKEN = os.getenv("BOT_SECRET_TOKEN")
APPLICATION_ID = os.getenv("BOT_APPLICATION_ID")

PREFIX = "!"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, status=discord.Status.idle, activity=discord.Game(name="Bot Activities"), application_id=APPLICATION_ID)

@bot.event   
async def on_ready():
    print(f"{bot.user} is ready!")

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
@is_owner()
async def sync(ctx):
    print("is owner confirmed")
    try:
        await ctx.bot.tree.sync()
        print("tree synced")
        await ctx.send("Commands are synced!")
    except Exception as e:
        print("Error during sync:", e)
        await ctx.send("An error occurred during sync.")

async def load():
    for file in os.listdir(os.path.join(project_root, 'src', 'cogs')):
        if file.endswith('.py'):
            await bot.load_extension(f'src.cogs.{file[:-3]}')

async def main():
    await load()
    await bot.start(TOKEN)
    
asyncio.run(main())
