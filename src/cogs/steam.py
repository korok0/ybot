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
pSumUrl = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_KEY}&steamids="

class SteamCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("steam cog loaded!")

    # add confirmation later
    @app_commands.command(name="unlink", description="unlinks your steam profile")
    async def unlink(self, interaction: discord.Interaction):
        embed = discord.Embed(color=discord.Color.blue(), title="Do you wish to unlink your account?")
        await interaction.response.send_message(view=SteamButton(interaction), embed=embed)
        


    @app_commands.command(name='steamprofile', description="gets the steam profile of member")
    async def get_profile(self, interaction: discord.Interaction, member: discord.Member):
        url = pSumUrl
        aColor = discord.Colour.dark_theme()
        # bot cannot have profile
        view = None
        if member.id == interaction.client.user.id:
            embed = discord.Embed(color=aColor,
                                    title=f'Bot does not have a steam profile!')
        else: 
            # check if user is registered and if token is valid
            if u.is_registered(member.id) and u.test_token(member.id):
                b_token = u.fetch_token(member.id)
                # check if user 
                steam_id = u.get_user_steam_id(b_token)
                embed = discord.Embed(color=aColor,
                                title=f'User must add steam to their connections in **settings > connections**')
                if steam_id is not None:
                    # unpack steam data
                    url+=steam_id
                    data = u.get_steam_data(url)
                    avatar, name, country, profile_url, time_created = (u.unpack(0, data, 'avatarfull'), 
                            u.unpack(0, data, 'personaname'), u.unpack(0, data, 'loccountrycode'), 
                            u.unpack(0, data, 'profileurl'), u.unpack(0, data, "timecreated"))
                    if len(country) == 2: country = f":flag_{country.lower()}:"

                    embed = discord.Embed(colour=aColor,title=f'{name}\'s profile', url=profile_url, description=f"**Country:** {country}").add_field(name=f"**__Created__** ", 
                        value=f"{datetime.utcfromtimestamp(int(time_created)).strftime('%b %d %Y')}").set_thumbnail(url=avatar)
                    view = SteamSelectMenu(interaction=interaction, embed=embed)
            else:
                embed = discord.Embed(color=aColor,
                                title=f'User must register their account by using **/register** command')
        embed.set_author(name=member.name, icon_url=member.avatar)
        await interaction.response.send_message(embed=embed, view=view)
            
        

        
async def setup(bot):
    await bot.add_cog(SteamCommands(bot))