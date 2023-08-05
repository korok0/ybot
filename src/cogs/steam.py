import discord
from discord.ext import commands
from discord import app_commands
import sys
project_root = 'C:\\Users\\Vinea\\Desktop\\Personal Projects\\ybot'
sys.path.append(project_root)
from src.buttons.buttons import SteamButton
from src.utils.utility import Utility
from dotenv import load_dotenv
import os
from datetime import datetime
import sqlite3
import time
load_dotenv()
u = Utility()
STEAM_KEY = os.getenv("STEAM_SECRET_TOKEN")
pSumUrl = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_KEY}&steamids="
conn = sqlite3.connect("C:\\Users\\Vinea\\Desktop\\Personal Projects\\ybot\\src\\bot\\members.db", check_same_thread=False)
c = conn.cursor()

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
    async def getProfile(self, interaction: discord.Interaction, member: discord.Member):
        url = pSumUrl
        aColor = discord.Colour.dark_theme()
        if member.id == interaction.client.user.id:
            embed = discord.Embed(color=aColor,
                                    title=f'Bot does not have a steam profile!')
            ephVar = False
        else: 
            if u.is_registered(member.id) and u.test_token(member.id):
    
                b_token = u.fetch_token(member.id)
                if u.get_user_steam(b_token) is None:
                    embed = discord.Embed(color=aColor,
                                    title=f'User must add steam to their connections in settings>connections')
                    ephVar = False
                else:
                    steam_id = u.get_user_steam(b_token)
                    url+=steam_id
                    avatar = u.unpack(0, url, 'avatarfull')

                    name = u.unpack(0, url, 'personaname')
                    try:
                        last_on = u.unpack(0, url, 'lastlogoff')
                    except Exception as e:
                        print(f"new account error: {e}\nUsing current time")
                        last_on = time.time()
                    profile_url = u.unpack(0, url, 'profileurl')
                    embed = discord.Embed(colour=aColor,title=f'{name}\'s profile', url=profile_url, description=f"Last on: {datetime.utcfromtimestamp(int(last_on)).strftime('%b %d %Y')}")
                    embed.set_thumbnail(url=avatar)
                    ephVar = False
            else:
                if member.id == interaction.user.id:
                # will send user to register/authenticate their account into the database
                    ephVar = True
                    embed = discord.Embed(color=aColor,
                                        title=f'User does not have an account linked. Click to register',
                                        url='https://discord.com/api/oauth2/authorize?client_id=1027772366476017677&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fe&response_type=code&scope=identify%20connections')
                else:
                    embed = discord.Embed(color=aColor,
                                    title=f'User must register their account by using /register command (WIP)')
                    ephVar = False
        embed.set_author(name=member.name, icon_url=member.avatar)
        await interaction.response.send_message(embed=embed, ephemeral=ephVar)
    # app_command register
        
async def setup(bot):
    await bot.add_cog(SteamCommands(bot))