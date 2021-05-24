import discord
import requests
from discord.ext import commands





class Actions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def wink(self, ctx, user: discord.Member = None):
        if user == None:
            await ctx.message.reply(f"Who are you winking at? Mention someone next time!")
            return

        if user == ctx.author:
            await ctx.message.reply(f"Why are you so lonely? Don't wink at yourself!")
            return

        if user == self.client.user:
            await ctx.message.reply(f":flushed: Did you just wink at me?")
            return

        url = "https://some-random-api.ml/animu/wink"
        response = requests.get(url)
        wink = response.json()

        embed = discord.Embed(
            title="da vinky",
            description=f"{ctx.author.mention} just winked at {user.mention}",
            color=discord.Colour.random() 
        )
        embed.set_image(url=wink['link'])
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def hug(self, ctx, user: discord.Member = None):
        if user == None:
            await ctx.message.reply(f"Why are you so lonely? Mention someone that you wanna hug, you can't hug yourself :(")
            return

        if user == ctx.author:
            await ctx.message.reply("Imagine hugging yourself... why are you so lonely")
            return

        if user == self.client.user:
            await ctx.message.reply(f"Aww thanks for the hug! <3")
            return

        embed = discord.Embed(
            title="aww hugs uwu",
            description=f"this is so cute >< {ctx.author.mention} just hugged {user.mention}",
            color=discord.Colour.random() 
        )
        embed.set_image(url=requests.get(
            "https://nekos.life/api/hug").json()['url'])

        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def kiss(self, ctx, user: discord.Member = None):
        if user == None:
            await ctx.message.reply(f"Why are you so lonely? Mention someone that you wanna kiss, you can't kiss yourself :(")
            return

        if user == ctx.author:
            await ctx.message.reply("Imagine kissing yourself... loser")
            return

        if user == self.client.user:
            await ctx.message.reply(f"*Kisses back*")
            return

        embed = discord.Embed(
            title="mwah",
            description=f"{ctx.author.mention} just kissed {user.mention}",
            color=discord.Colour.random() 
        )
        embed.set_image(url=requests.get(
            "https://nekos.life/api/kiss").json()['url'])

        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def pat(self, ctx, user: discord.Member = None):
        if user == None:
            await ctx.message.reply(f"Why are you so lonely? Mention someone that you wanna pat, you can't pat yourself :(")
            return

        if user == ctx.author:
            await ctx.message.reply("Imagine patting yourself...noob")
            return

        if user == self.client.user:
            await ctx.message.reply(f"Thank you for patting ><")
            return

        embed = discord.Embed(
            title="*cute pats*",
            description=f":flushed: {ctx.author.mention} just patted {user.mention}",
            color=discord.Colour.random() 
        )
        embed.set_image(url=requests.get(
            "https://nekos.life/api/pat").json()['url'])

        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def slap(self, ctx, user: discord.Member = None):
        if user == None:
            await ctx.message.reply(f"Who do you want to slap idiot? Mention it next time.")
            return

        if user == ctx.author:
            await ctx.message.reply("Imagine slapping yourself...masochist")
            return

        if user == self.client.user:
            await ctx.message.reply("looool get owned")
            return

        embed = discord.Embed(
            title="haha noob",
            description=f"{user.mention} just got slapped by {ctx.author.mention}.",
            color=discord.Colour.random() 
        )
        embed.set_image(url=requests.get(
            "https://nekos.life/api/v2/img/slap").json()['url'])

        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def tickle(self, ctx, user: discord.Member = None):
        if user == None:
            await ctx.message.reply(f"Who do you want to tickle idiot? Mention it next time.")
            return

        if user == ctx.author:
            await ctx.message.reply("ur werid..periodt")
            return

        if user == self.client.user:
            await ctx.message.reply(f"dont tickle me creep.")
            return

        embed = discord.Embed(
            title="Tickle, tickle!",
            description=f"{user.mention} just got tickled by {ctx.author.mention}.",
            color=discord.Colour.random() 
        )
        embed.set_image(url=requests.get(
            "https://nekos.life/api/v2/img/tickle").json()['url'])

        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def facepalm(self, ctx):
        url = "https://some-random-api.ml/animu/face-palm"
        response = requests.get(url)
        facepalm = response.json()

        embed = discord.Embed(
            title="Bruh",
            description=f"{ctx.author.mention} just facepalmed",
            color=discord.Colour.random() 
        )
        embed.set_image(url=facepalm['link'])
        await ctx.send(embed=embed)


def setup(client):
	client.add_cog(Actions(client))
