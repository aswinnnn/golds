import discord
from discord.ext import commands
import json
import random
import requests

clr = [discord.Color.dark_orange(),discord.Color.orange(),discord.Color.dark_gold(),discord.Color.gold(),discord.Color.dark_magenta(),discord.Color.magenta(),discord.Color.red(),discord.Color.dark_red(),discord.Color.blue(),discord.Color.dark_blue(),discord.Color.teal(),discord.Color.dark_teal(),discord.Color.green(),discord.Color.dark_green(),discord.Color.purple(),discord.Color.dark_purple()]

class Jokes(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command(pass_context=True)
	async def joke(self, ctx):
		url = "https://joke3.p.rapidapi.com/v1/joke"
		# i think this api doesnt work anymore, you might have to use another one, there are 100s of em out there for free.
		querystring = {"nsfw": "true"}
		headers = {'x-rapidapi-key': "",'x-rapidapi-host': ""}
		response = requests.request("GET", url,headers=headers, params=querystring)
		jokedict = json.loads(response.text)
		joke = jokedict["content"]
		embed5 = discord.Embed(description='**{}**'.format(joke),color=random.choice(clr))
		await ctx.send(embed=embed5)

def setup(bot):
		bot.add_cog(Jokes(bot))
		