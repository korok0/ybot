import discord
from discord.ext import commands
from discord import app_commands
import sys

from discord.interactions import Interaction
project_root = 'C:\\Users\\Vinea\\Desktop\\Personal Projects\\ybot'
sys.path.append(project_root)
from src.utils.utility import Utility

u = Utility()
class SteamButton(discord.ui.View):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.cmd_interaction_user = interaction.user
        self.member_id = interaction.user.id
        print("initialized")
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.interaction.user:
            embed = discord.Embed(color=discord.Color.yellow(), title=f"Try using your own /{self.interaction.command.name}")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return True
    
    @discord.ui.button(label="confirm", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, Button: discord.ui.Button):
        print("debug1")
        print(self.interaction.user.id)
        
        if interaction.user.id == self.member_id:
            Button.disabled = True
            if u.unregister(self.interaction.user.id):
                title = "Confirmed unlinking..!"
                embedColor = discord.Color.green()
                print("after unreg")
            else:
                title = "You are not registered..."
                embedColor = discord.Color.dark_grey()
        
            embed = discord.Embed(color=embedColor, title=title)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            if interaction.response.is_done():
                await interaction.message.delete()
    
    @discord.ui.button(label="cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, Button: discord.ui.Button):
        embed = discord.Embed(color=discord.Color.red(), title="Canceled unlinking..!")
        if interaction.user.id == self.member_id:
            Button.disabled = True
            await interaction.response.send_message(embed=embed, ephemeral=True)
            if interaction.response.is_done():
                await interaction.message.delete()
        
        