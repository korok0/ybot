import discord
import sys
import os
from collections import deque

project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\.."))
print(f"PR Buttons: {project_root}")
sys.path.append(project_root)

from src.utils.utility import Utility

STEAM_KEY = os.getenv("STEAM_SECRET_TOKEN")
u = Utility()

class SteamSelectMenu(discord.ui.View):
    # pass in app_command interaction so that we can manipulate it
    def __init__(self, interaction: discord.Interaction, embed: discord.Embed, steam_id: str):
        """
        :param interaction: command's original `discord.Interaction`
        :param embed: command's original `discord.Embed` in this case it is the User Profile embed page
        
        """
        super().__init__()
        self.embed = embed
        self.interaction = interaction
        self.steam_id = steam_id
    
    @discord.ui.select(options=[
        discord.SelectOption(label="Recently Played"),
        discord.SelectOption(label="User Profile")
    ], placeholder="Info")
    async def select_page(self, interaction: discord.Interaction, option: discord.ui.Select):
        # default page is user profile denoted by this embed
        embed = self.embed
        if option.values[0] == "Recently Played":
            url = f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={STEAM_KEY}&steamid={self.steam_id}&count=1"
            data = u.get_steam_data(url)
            game_name = u.unpack(0, data, 'name', 'games')
            url_hash = u.unpack(0, data, 'img_icon_url', 'games')
            app_id = u.unpack(0, data, 'appid', 'games')
            # rpg = u.unpack()
            embed = discord.Embed(
                color=discord.Color.dark_theme(),
                title=game_name, url=f"https://store.steampowered.com/app/{app_id}")
            embed.set_thumbnail(url=f"https://media.steampowered.com/steamcommunity/public/images/apps/{app_id}/{url_hash}.jpg")
        await interaction.message.edit(embed=embed, view=self)
        await interaction.response.defer()