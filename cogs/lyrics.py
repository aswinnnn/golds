import discord
from discord.ext import commands
import json
import random
import requests


class Lyrics(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		

	  
	
	@commands.command() 
	async def lyrics(self,ctx, *, song):
	  
	  headers = {'User-agent': 'goldsy grr sksk v20 Linux'}
	  	
	  url = f"https://some-random-api.ml/lyrics?title={song}"
	  
	  res = requests.get(url, headers=headers).json() 
	  title = res["title"]
	  author = res["author"]
	  lyrics = str(res["lyrics"]) 
	  image = res["thumbnail"]["genius"]
	  link = res["links"]["genius"]
	  
	  # apparently im dumb at seperating long lyrics to a number of embeds, if you have a better method, please use so.
	  if len(lyrics) > 1999:
	    lyrics1 = lyrics[:2000]
	    lyrics2 = lyrics[2000:]
	    embed = discord.Embed(title=title, url=link, description=lyrics1, color=discord.Colour.random())
	    embed.set_thumbnail(url=image)
	    await ctx.send(embed=embed)
	    embed = discord.Embed(title=title, url=link, description=lyrics2, color=discord.Colour.random())
	    embed.set_thumbnail(url=image)
	    await ctx.send(embed=embed)
	    return 
	  embed = discord.Embed(title=title, url=link, description=lyrics, color=discord.Colour.random())
	  embed.set_thumbnail(url=image)
	  await ctx.send(embed=embed)


def setup(bot):
  bot.add_cog(Lyrics(bot))    
	    
	    