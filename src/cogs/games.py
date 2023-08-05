from discord.ext import commands
import random
import discord
from discord import app_commands
import requests

class Games(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print("games cog loaded!")

	@app_commands.command(name="cat", description="Sends image of cat")
	async def requestCat(self, interaction: discord.Interaction) -> None:
		cat_url = "https://api.thecatapi.com/v1/images/search"
		res = requests.get(cat_url)
		data = res.json()
		first_item = data[0]
		cat_image = first_item['url']
		print(cat_image)
		embed = discord.Embed(color=discord.Colour.random())
		embed.set_image(url=cat_image)
		await interaction.response.send_message(embed=embed)

	@app_commands.command(name="speak")
	async def speak(self, interaction: discord.Interaction) -> None:
		await interaction.response.send_message("Speaking")

	@app_commands.command(name="pong", description="This command pongs")
	async def pong(self, interaction: discord.Interaction, member: discord.Member, reason: str="No reason entered"):
		await interaction.response.send_message(f'Pings! {member.mention}')
		print(reason)

	@app_commands.command(name="coinflip", description="Flips a coin")
	@app_commands.choices(face=[
		discord.app_commands.Choice(name="heads", value=1),
		discord.app_commands.Choice(name="tails", value=2)])
	async def coinflip(self, interaction: discord.Interaction, face: discord.app_commands.Choice[int]) -> None:
		choices = ["heads", "tails"]

		print(face.name)
		choice = random.choice(choices)
		if face.name == choice:
			answer = f"You **win!** {interaction.user.mention}"
			aColor =  discord.Colour.brand_green()
		else:
			answer = f"You **lose!** {interaction.user.mention}"
			aColor =  discord.Colour.brand_red()
		embed = discord.Embed(description=f'The coin landed on **{choice}**!\n{answer}', color=aColor)
		embed.set_author(name='Coinflip', icon_url='https://thumbs.gfycat.com/TerribleTepidArmedcrab-max-1mb.gif')
		await interaction.response.send_message(embed=embed)

async def setup(bot):
	await bot.add_cog(Games(bot))