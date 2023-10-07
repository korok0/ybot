import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from datetime import datetime

project_root = os.getcwd()
print(f"PR Steam: {project_root}")


from src.views.buttons import SteamButton
from src.views.selectmenus import SteamSelectMenu
from src.utils.utility import Utility

load_dotenv()
u = Utility()
STEAM_KEY = os.getenv("STEAM_SECRET_TOKEN")
BOT_OAUTH_LINK = os.getenv("BOT_OAUTH_LINK")
pSumUrl = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_KEY}&steamids="

class SteamCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("steam cog loaded!")

    # add confirmation later
    @app_commands.command(name="unlink", description="unlinks your connections from bot")
    async def unlink(self, interaction: discord.Interaction):
        embed = discord.Embed(color=discord.Color.blue(), title="Do you wish to unlink your account?")
        await interaction.response.send_message(view=SteamButton(interaction=interaction, type='unlink'), embed=embed)
    
    @app_commands.command(name="link", description="links your connections to bot")
    async def link(self, interaction: discord.Interaction):
        embed = discord.Embed(color=discord.Color.green(), title="Link your account", url=BOT_OAUTH_LINK)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    @app_commands.command(name='steamprofile', description="gets the steam profile of member")
    async def get_profile(self, interaction: discord.Interaction, member: discord.Member):
        a_color = discord.Colour.dark_theme()

        # variable that keeps track if interaction has already been responded to
        followup = False
        
        # bot cannot have profile
        view = None
        if member.bot:
            embed = discord.Embed(color=discord.Color.dark_theme(), title='**bots** cannot have steam accounts!')
            embed.set_footer(text=member.name, icon_url=member.avatar)
            
        else:
            if u.is_registered(member.id) and u.test_token(member.id):
                b_token = u.fetch_token(member.id)
                steam_id = u.get_user_steam_id(b_token)

                # if steam_id not in database
                if steam_id is None:
                    embed = discord.Embed(color= a_color, title=f'User must add steam to their connections in **settings > connections**')

                else:
                    await interaction.response.defer()
                    followup = True
                    p_sum_url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_KEY}&steamids="
                    game_url = f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={STEAM_KEY}&steamid={steam_id}&count=1"

                    # unpack steam data
                    p_sum_url+=steam_id
                    data = u.get_steam_data(p_sum_url)
                    game_data = u.get_steam_data(game_url)

                    # unpack steam details
                    avatar, name, country, profile_url, time_created = (
                        u.unpack_steam(0, data, 'avatarfull', 'players'), 
                        u.unpack_steam(0, data, 'personaname', 'players'), 
                        u.unpack_steam(0, data, 'loccountrycode', 'players'), 
                        u.unpack_steam(0, data, 'profileurl', 'players'), 
                        u.unpack_steam(0, data, 'timecreated', 'players'))
                    
                    # turn country code into country flag emoji
                    if len(country) == 2: country = f":flag_{country.lower()}:"

                    embed = discord.Embed(color= a_color, title= f'{name}\'s profile', url=profile_url, description=f"**Country:** {country}").add_field(name=f"**__Created__** ", 
                        value=f"{datetime.utcfromtimestamp(int(time_created)).strftime('%b %d %Y')}").set_thumbnail(url=avatar).set_footer(text=member.name, icon_url=member.avatar)
                    view = SteamSelectMenu(interaction=interaction, embed=embed, steam_id=steam_id, data=game_data, member=member)
                    await interaction.followup.send(embed=embed, view=view)

            # if user is not registered        
            else:
                embed = discord.Embed(color=a_color, title='User must register their account by using **/link** command')
                
        # to avoid "interaction already responded to" error even if it is already handled by discord py
        # to avoid duplicate interaction messages
        if followup == False:
            await interaction.response.send_message(embed=embed)
            
async def setup(bot):
    await bot.add_cog(SteamCommands(bot))