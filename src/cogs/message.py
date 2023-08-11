import discord
from discord.ext import commands
from discord import app_commands
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\.."))
print(f"PR Message: {project_root}")
sys.path.append(project_root)

class MessageCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("message cog loaded!")
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        memb = message.author
        channel = self.bot.get_channel(1130593170053398581)
        mlog = f"Message sent by <@{memb.id}> deleted in <#{message.channel.id}>\n**Contents:** {message.content}"
        embed = discord.Embed(description = mlog, color = discord.Colour.random())
        embed.set_author(name=memb.name,icon_url=message.author.avatar)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        pass

async def setup(bot):
    await bot.add_cog(MessageCog(bot))