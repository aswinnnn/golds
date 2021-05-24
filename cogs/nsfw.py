import discord
import requests
import datetime
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import (CommandOnCooldown)
from discord.ext import commands


# u naughty naughty 

class NSFW(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Fuck someone! LUL")
    async def fuck(self, ctx, user: discord.Member = None):
        if ctx.channel.is_nsfw():
            if user == None:
                await ctx.message.reply("Who do you want to fuck? Mention them next time idiot.")
                return

            if user == ctx.author:
                await ctx.message.reply("Don't fuck yourself smh")
                return

            response = requests.get(
                "https://api.neko-chxn.xyz/v1/fuck/img").json()

            embed = discord.Embed(
                title="mmmm",
                description=f"{user.mention} got fucked hard by {ctx.author.mention}",
                color=discord.Colour.random()
            )
            embed.set_image(url=response['url'])
            await ctx.message.reply(embed=embed)
        else:
            embed = discord.Embed(
                title = "Go away horny!",
                description = "This command can only be using in a NSFW channel.",
                color = 0xFFC0CB
            )
            embed.set_footer(text="Idiot!")
            await ctx.message.reply(embed=embed)


    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def spank(self, ctx, user: discord.Member = None):
        if ctx.channel.is_nsfw():
            if user == None:
                await ctx.message.reply("Who do you want to spank? Mention them next time idiot.")
                return

            if user == ctx.author:
                await ctx.message.reply("How lonely are you? Don't spank yourself!")
                return

            response = requests.get("https://nekos.life/api/v2/img/spank").json()

            embed = discord.Embed(
                title = ":weary:",
                description = f"{user.mention} got spanked by {ctx.author.mention}",
                color = 0xFFC0CB
            )
            embed.set_image(url = response['url'])
            await ctx.message.reply(embed = embed)
        else:
            await ctx.message.reply("This command can only be used in a NSFW channel.")

def setup(client):
    client.add_cog(NSFW(client))
