import discord 
from discord.ext import commands
import datetime
from dateutil.relativedelta import relativedelta

start_time = datetime.datetime.now().time().strftime('%H:%M:%S')

class Startup(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	       
	@commands.command()
	async def ping(self, ctx):
		
		msg = await ctx.send("checking ping...")
		await msg.delete()
		await ctx.send(f'pong bitch ` {round(self.bot.latency * 100)}ms `')
	       
	@commands.command(pass_context=True, aliases=['ut', 'since'])
	async def uptime(self, ctx):
		
		end_time = datetime.datetime.now().time().strftime('%H:%M:%S')
		started = datetime.datetime.strptime(start_time, "%H:%M:%S")
		rightNow = datetime.datetime.strptime(end_time, "%H:%M:%S")
		upTime = relativedelta(started, rightNow)
		days = upTime.days
		hours = upTime.hours
		mins = upTime.minutes
		secs = upTime.seconds
		embed = discord.Embed(
		title="Bot Uptime",description=f" The bot has been online for {abs(days)} days, {abs(hours)} hours,  {abs(mins)} minutes, {abs(secs)} seconds",color=0x52bf90)
		embed.set_thumbnail(url="https://images.emojiterra.com/google/android-nougat/512px/23f3.png")
		await ctx.send(embed=embed)

   
	
def setup(bot):
      bot.add_cog(Startup(bot))
       
     
    

  
		
	