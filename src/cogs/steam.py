import discord
from discord.ext import commands
from discord import app_commands
import sys
import os
from dotenv import load_dotenv
from datetime import datetime
import time

project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\.."))
print(f"PR Steam: {project_root}")
sys.path.append(project_root)

from src.views.buttons import SteamButton
from src.views.selectmenus import SteamSelectMenu
from src.utils.utility import Utility

load_dotenv()
u = Utility()
STEAM_KEY = os.getenv("STEAM_SECRET_TOKEN")
BOT_OAUTH_LINK = os.getenv("BOT_OAUTH_LINK")
pSumUrl = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_KEY}&steamids="

class SteamCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("steam cog loaded!")

    # add confirmation later
    @app_commands.command(name="unlink", description="unlinks your connections from bot")
    async def unlink(self, interaction: discord.Interaction):
        embed = discord.Embed(color=discord.Color.blue(), title="Do you wish to unlink your account?")
        await interaction.response.send_message(view=SteamButton(interaction, 'unlink'), embed=embed)
    
    @app_commands.command(name="link", description="links your connections to bot")
    async def link(self, interaction: discord.Interaction):
        embed = discord.Embed(color=discord.Color.green(), title="Link your account", url=BOT_OAUTH_LINK)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    @app_commands.command(name='steamprofile', description="gets the steam profile of member")
    async def get_profile(self, interaction: discord.Interaction, member: discord.Member):
        a_color = discord.Colour.dark_theme()
        # bot cannot have profile
        view = None
        # check if user is registered and if token is valid
        if u.is_registered(member.id) and u.test_token(member.id):
            b_token = u.fetch_token(member.id)
            # check if user 
            steam_id = u.get_user_steam_id(b_token)
            embed = discord.Embed(color=a_color,
                            title=f'User must add steam to their connections in **settings > connections**')
            if steam_id is not None:
                p_sum_url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_KEY}&steamids="
                game_url = f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={STEAM_KEY}&steamid={steam_id}&count=1"
                # unpack steam data
                p_sum_url+=steam_id
                data = u.get_steam_data(p_sum_url)
                game_data = u.get_steam_data(game_url)
                avatar, name, country, profile_url, time_created = (u.unpack(0, data, 'avatarfull', 'players'), 
                        u.unpack(0, data, 'personaname', 'players'), u.unpack(0, data, 'loccountrycode', 'players'), 
                        u.unpack(0, data, 'profileurl', 'players'), u.unpack(0, data, 'timecreated', 'players'))
                if len(country) == 2: country = f":flag_{country.lower()}:"

                embed = discord.Embed(colour=a_color,title=f'{name}\'s profile', url=profile_url, description=f"**Country:** {country}").add_field(name=f"**__Created__** ", 
                    value=f"{datetime.utcfromtimestamp(int(time_created)).strftime('%b %d %Y')}").set_thumbnail(url=avatar)
                view = SteamSelectMenu(interaction=interaction, embed=embed, steam_id=steam_id, data=game_data, member=member)
        else:
            embed = discord.Embed(color=a_color,
                            title=f'User must register their account by using **/link** command')
        embed.set_author(name=member.name, icon_url=member.avatar)
        await interaction.response.send_message(embed=embed, view=view)
            
async def setup(bot):
    await bot.add_cog(SteamCommands(bot))