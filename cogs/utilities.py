import discord
from discord.ext import commands
import time
import random
import requests
import asyncio
import json


trigs = ["goldy","Goldy", "GOldy", "GOLdy", "GOLDY","g*ldy", "goldY"]
kates = ["139111399556120576", "kate","KATE"]

class Utilities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.Cog.listener()
	async def on_ready(self):
	   print('Logged in as:')
	   print(self.bot.user.name)
	   print('-------------')
	   print(f'ID:{self.bot.user.id}')
	   print('-------------')
	   print('-------------')
	   print(f'successfully connected to {len(self.bot.guilds)} servers')
	   
	   
	   
	
	@commands.command(pass_context=True)
	async def bans(self, ctx):
	   	banlist = await ctx.guild.bans()
	   	banned = len(banlist)
	   	embed = discord.Embed(description=f"Total number of banned users: **{banned}** ")
	   	embed.set_footer(text="get beaned")
	   	await ctx.send(embed=embed)
			
	@commands.Cog.listener()
	async def on_message(self, message):
	       
	       if message.author == self.bot.user:
	       	return
	       	
	       if "welc" in message.content.lower() and message.guild.id == 741611893260812288:
	       	em = self.bot.get_emoji(828301600938000424)
	       	em1 = self.bot.get_emoji(828301554641010738)
	       	await message.add_reaction(em)
	       	await message.add_reaction(em1)
	       	
	       	
	       	
	       for trig in trigs:
	       	if trig in message.content.lower():
	       		emoji = self.bot.get_emoji(821377584104341545)
	       		await message.add_reaction(emoji)
	       for kate in kates:
	       	if kate in message.content.lower():
	       		await message.reply("<:cc_lipbite:810616801863663656>")
	       		
	       	if "deku" in message.content.lower() and message.guild.id == 741611893260812288:
	       		emoji = self.bot.get_emoji(828302415551528960)
	       		emoji2 = self.bot.get_emoji(828302364556787733)
	       		await message.add_reaction(emoji)
	       		await message.add_reaction(emoji2)
	       		
	       	if "golds" in message.content.lower():
	       				'''
	       				
	       				orgmsg = message
	       				msgstuff = []
	       				async for message in message.channel.history(limit=100):
	       					msgstuff.append(message.clean_content)
	       					if message.author.bot == True:
	       						msgstuff.remove(message.clean_content)
	       				msgs = []
	       				for msg in msgstuff:
	       							if msg:
	       								msgs.append(msg)
	       				msgnum = int(len(msgs))
	       				num = msgnum - 1
	       				randomnum = random.randrange(1, num)
	       				randommsg = msgs[randomnum]
	       				await orgmsg.reply(f"{randommsg}")
	       				'''
	       				words = message.content.lower()
	       						
	       				msg = words.replace("golds", "")
	       				try:
	       					response = requests.get(f"https://rdch.dev64.repl.co/chat?message={msg}").json()['reply']
	       					await message.reply(f"{response}")
	       					return
	       				except:
	       					await message.reply("`golds couldnt process that.`")
	       					return
	       				
	   	

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
			if  isinstance(error, commands.CommandNotFound):
				return
			if "TimeoutError" in str(error):
				return
			msg = await ctx.send(f"```py\n{error}\n```")
			await asyncio.sleep(5)
			await msg.delete()
		
		
		

	       


def setup(bot):
		bot.add_cog(Utilities(bot))
		

		
