import discord
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\.."))
print(f"PR Buttons: {project_root}")
sys.path.append(project_root)

from src.utils.utility import Utility

u = Utility()
class SteamButton(discord.ui.View):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.member_id = interaction.user.id
        self.is_pressed = False
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.is_pressed == True:
            print("Buttons are disabled!")
            embed = discord.Embed(color=discord.Color.yellow(), title=f"Choice already made")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif interaction.user != self.interaction.user:
            embed = discord.Embed(color=discord.Color.yellow(), title=f"Try using your own /{self.interaction.command.name}")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return True
    
    @discord.ui.button(label="confirm", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == self.member_id and self.is_pressed==False:
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
                self.is_pressed = True
                await interaction.message.delete()
                
    
    @discord.ui.button(label="cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, Button: discord.ui.Button):
        embed = discord.Embed(color=discord.Color.red(), title="Canceled unlinking..!")
        if interaction.user.id == self.member_id and self.is_pressed==False:
            await interaction.response.send_message(embed=embed, ephemeral=True)
            if interaction.response.is_done():
                self.is_pressed = True
                await interaction.message.delete()
                
        
        