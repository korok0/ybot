import discord
import sys
import os
from collections import deque

project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\.."))
print(f"PR Buttons: {project_root}")
sys.path.append(project_root)

from src.utils.utility import Utility

class SteamSelectMenu(discord.ui.View):
    # pass in app_command interaction so that we can manipulate it
    def __init__(self, interaction: discord.Interaction, embed: discord.Embed):
        """
        :param interaction: command's original `discord.Interaction`
        :param embed: command's original `discord.Embed` in this case it is the User Profile embed page
        
        """
        super().__init__()
        self.embed = embed
        self.interaction = interaction
    
    @discord.ui.select(options=[
        discord.SelectOption(label="Recently Played Games"),
        discord.SelectOption(label="User Profile")
    ])
    async def select_page(self, interaction: discord.Interaction, option: discord.ui.Select):
        if option.values[0] == "User Profile": 
            await interaction.message.edit(embed=self.embed, view=self)
            await interaction.response.defer()
        else:
            embed = discord.Embed(
                color=discord.Color.dark_theme(),
                title= option.values[0]
            )
            await interaction.message.edit(embed=embed, view=self)
            await interaction.response.defer()