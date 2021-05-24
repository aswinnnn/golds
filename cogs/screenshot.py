import discord
import os
from discord.ext import commands
import requests

class ScreenShot(commands.Cog , name ="WebScreenShot"):
  
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command(aliases=['ss'])
  @commands.is_owner()
  async def screenshot(self, ctx , *,text):
    blocked = ['porn', 'hentai', 'hanime.tv', 'redtube', 'xvideos', 'xxx', 'xhamster', 'chaturbate', 'cock', 'brazzers', 'pussy']
    
    for site in blocked:
      if site in str(text):
        await ctx.send("you cant search that hoe")
        return
        
    SECRET_TOKEN_OMEGALUL = ""
    
    if True:
      link = ""
      text_new = text
      
      if text.startswith('http://') or text.startswith('https://'):
        pass
      
      else:
        text_new = f"https://{text}"
        
      try:
        a = requests.get(text_new)
        link = text_new
        
      except:
        link = f"https://www.google.com/search?q={text}"
        
      api = f"https://v2.convertapi.com/convert/web/to/jpg?Secret={SECRET_TOKEN_OMEGALUL}&Url={link}&StoreFile=true&ImageHeight=800&ConversionDelay=1&AdBlock=true&CookieConsentBlock=true"
      
      x = requests.get(api)
      img_url = x.json()["Files"][0]["Url"]
      img_data = requests.get(img_url).content
      with open('google.jpg', 'wb') as handler:
        handler.write(img_data)
        
      await ctx.send(ctx.author.mention, file = discord.File('google.jpg'))
      
      
def setup(bot):
  bot.add_cog(ScreenShot(bot))
