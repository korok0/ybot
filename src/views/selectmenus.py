import discord
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\.."))
print(f"PR Buttons: {project_root}")
sys.path.append(project_root)

from src.utils.utility import Utility

class SteamSelectMenu(discord.ui.View):
    # pass in app_command interaction so that we can manipulate it
    def __init__(self, interaction: discord.Interaction):
        super().__init__()
        self.interaction = interaction
    
    @discord.ui.select(options=[
        discord.SelectOption(label="Recently Played Games"),
        discord.SelectOption(label="User Profile")
    ])
    async def select_page(self, interaction: discord.Interaction, option: discord.ui.Select):
        if option.values[0] == "User Profile": 
            await self.interaction.edit_original_response(content="hey")
        else:
            await interaction.response.send_message("if failed")