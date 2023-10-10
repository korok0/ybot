import discord
import sys
import os
from collections import deque
from typing import Any

project_root = os.getcwd()
print(f"PR SelectMenu: {project_root}")

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
                game_name, url_hash, app_id, playtime_2weeks, playtime_forever  = (u.unpack_steam(0, data, 'name', 'games'), u.unpack_steam(0, data, 'img_icon_url', 'games'), u.unpack_steam(0, data, 'appid', 'games'),
                                                            u.unpack_steam(0, data, 'playtime_2weeks', 'games'), u.unpack_steam(0, data, 'playtime_forever', 'games'))
                
                # do something with game stats ------------------#
                game_stats_url = f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={app_id}&key={STEAM_KEY}&steamid={self.steam_id}"
                game_stats: dict = u.get_steam_data(url=game_stats_url)

                playtime_2weeks, unit_2weeks = self._convert_time(playtime_2weeks)
                playtime_forever, unit_forever = self._convert_time(playtime_forever)

                embed = discord.Embed(
                    color=discord.Color.dark_theme(),
                    title=game_name, url=f"https://store.steampowered.com/app/{app_id}", description=f"**Time Played Past Two Weeks:** {playtime_2weeks:.2f} {unit_2weeks}\n**Total Time Played:** {playtime_forever:.2f} {unit_forever}")
                embed.set_thumbnail(url=f"https://media.steampowered.com/steamcommunity/public/images/apps/{app_id}/{url_hash}.jpg")
                if game_name == "Counter-Strike 2":
                    
                    """
                    stats: [{
                        name: total kills,
                        value: 1000
                    },
                    {
                        name: total mvps,
                        value: 10
                    }]

                    stats key gives us a list of dictionaries. Search for "value" key and value by checking the "name" key
                    """
                    total_kills = [item['value'] for item in game_stats['playerstats']['stats'] if item['name'] == 'total_kills'][0]
                    total_wins = [item['value'] for item in game_stats['playerstats']['stats'] if item['name'] == 'total_wins'][0]
                    embed.description += f"\n**Total wins:** {total_wins}\n**Total kills:** {total_kills}"

            else: 
                embed = discord.Embed(title="User has no games played recently")
            embed.set_footer(text=self.member.name, icon_url=self.member.avatar)
        await interaction.message.edit(embed=embed, view=self)
        await interaction.response.defer()
    def _convert_time(self, playtime: int):
        unit = "minute(s)"
        if playtime >= 60:
            playtime /= 60
            unit = "hour(s)"
        return playtime, unit