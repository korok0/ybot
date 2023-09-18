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
        self.log_channel = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("message cog loaded!")
    
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        memb = message.author
        if self.log_channel is not None:
            channel = self.log_channel
        else:
            channel = message.guild.owner
            await channel.send("Logs will be sent to owner DM until log channel is set")
        att = message.attachments
        embed = discord.Embed(description=f"Message sent by <@{memb.id}> deleted in <#{message.channel.id}>\n**Contents:** {message.content}",
                              color = discord.Colour.random()).set_author(name=memb.name, icon_url=message.author.avatar)
        
        # check if attatchment list is empty
        if len(att) != 0:
            embed.set_image(url=att[0].proxy_url)
        await channel.send(embed=embed)
    
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True, manage_channels=True)
    @app_commands.command(name="setlogs", description="sets message log channel")
    async def set_logs(self, interaction: discord.Interaction):
        self.log_channel = interaction.channel
        await interaction.response.send_message(content="Log channel set!", ephemeral=True)

    @set_logs.error
    async def set_logs_error(self, interaction: discord.Interaction, error: discord.app_commands.MissingPermissions):
        mp = "\n".join(error.missing_permissions)
        await interaction.response.send_message(embed=discord.Embed(title="missing permissions:",
            description=f"{mp}"), 
            ephemeral=True)
        
async def setup(bot):
    await bot.add_cog(MessageCog(bot))