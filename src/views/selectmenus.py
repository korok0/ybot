import discord
import sys
import os
from collections import deque
from typing import Any

project_root = os.getcwd()
#project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\.."))
print(f"PR SelectMenu: {project_root}")
#sys.path.append(project_root)

from src.utils.utility import Utility

STEAM_KEY = os.getenv("STEAM_SECRET_TOKEN")
u = Utility()

class SteamSelectMenu(discord.ui.View):
    # pass in app_command interaction so that we can manipulate it
    def __init__(self, interaction: discord.Interaction, embed: discord.Embed, steam_id: str, data, member: discord.Member):
        """
        :param interaction: command's original `discord.Interaction`
        :param embed: command's original `discord.Embed` in this case it is the User Profile embed page
        :param data: any sort of data passed through. Defaults to None
        :param member: `discord.Member` argument passed in command
        """
        super().__init__()
        self.embed = embed
        self.interaction = interaction
        self.steam_id = steam_id
        self.data = data
        self.member = member
    
    @discord.ui.select(options=[
        discord.SelectOption(label="Most Played Past 2 Weeks"),
        discord.SelectOption(label="User Profile")
    ], placeholder="Info")
    async def select_page(self, interaction: discord.Interaction, option: discord.ui.Select):
        # default page is user profile denoted by this embed
        embed = self.embed
        if option.values[0] == "Most Played Past 2 Weeks":
            data = self.data
            print(data)
            # check if response is empty
            if data["response"]["total_count"] != 0:
                game_name, url_hash, app_id, time_played = (u.unpack_steam(0, data, 'name', 'games'), u.unpack_steam(0, data, 'img_icon_url', 'games'), u.unpack_steam(0, data, 'appid', 'games'),
                                                            u.unpack_steam(0, data, 'playtime_2weeks', 'games'))
                min = "minutes"
                if min == 1: min = "minute"
                embed = discord.Embed(
                    color=discord.Color.dark_theme(),
                    title=game_name, url=f"https://store.steampowered.com/app/{app_id}", description=f"**Time Played:** {time_played} {min}")
                embed.set_thumbnail(url=f"https://media.steampowered.com/steamcommunity/public/images/apps/{app_id}/{url_hash}.jpg")
            else: 
                embed = discord.Embed(title="User has no games played recently")
            embed.set_footer(text=self.member.name, icon_url=self.member.avatar)
        await interaction.message.edit(embed=embed, view=self)
        await interaction.response.defer()