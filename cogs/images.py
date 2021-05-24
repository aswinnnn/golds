import discord
import requests
import aiohttp
from discord.ext import commands



class Images(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def redpanda(self, ctx):
        url = 'https://some-random-api.ml/img/red_panda'
        response = requests.get(url)
        img = response.json()

        embed = discord.Embed(title="Red Panda", color=discord.Colour.random() )
        embed.set_image(url=img['link'])
        await ctx.message.reply("red pandas are kinda endangered right now. donate to buy them food or something idk https://www.redpandanetwork.org/give/",embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=['pika'])
    async def pikachu(self, ctx):
        url = 'https://some-random-api.ml/img/pikachu'
        response = requests.get(url)
        img = response.json()

        embed = discord.Embed(title="Pika!", color=discord.Colour.random() )
        embed.set_image(url=img['link'])
        await ctx.message.reply(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def comment(self, ctx, *, msg=None):
        if msg == None:
            await ctx.message.reply(embed=discord.Embed(
                title="Error!",
                description=f"Incorrect Usage! Use like this: `,comment <text>`",
                color=discord.Colour.magenta() 
            ))
            return
        url = f"https://some-random-api.ml/canvas/youtube-comment?avatar={ctx.author.avatar_url_as(format='png')}&username={ctx.author.name}&comment={msg}"
        url = url.replace(" ", "%20")
        embed = discord.Embed(color=discord.Colour.random() )
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def wasted(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        url = f"https://some-random-api.ml/canvas/wasted?avatar={user.avatar_url_as(format='png')}"
        embed = discord.Embed(color=discord.Colour.random() )
        embed.set_image(url=url)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def gay(self, ctx, user: discord.Member= None):
      if user == None:
        user = ctx.author
        
      url = f"https://some-random-api.ml/canvas/gay?avatar={user.avatar_url_as(format='png')}"
      embed = discord.Embed(color=discord.Colour.random())
      embed.set_image(url=url)
      await ctx.send(embed=embed)
      
    @commands.command()
    async def glass(self, ctx, user: discord.Member= None):
      if user == None:
        user = ctx.author
        
      url = f"https://some-random-api.ml/canvas/glass?avatar={user.avatar_url_as(format='png')}"
      embed = discord.Embed(color=discord.Colour.random())
      embed.set_image(url=url)
      await ctx.send(embed=embed)
      
    


def setup(client):
    client.add_cog(Images(client))
