import discord
from discord.colour import Color
from discord.ext import commands
import aiosqlite as sql
from discord.ext.commands import BucketType
import asyncio
import datetime
import time 
from discord.ext.commands.core import is_owner
import random 

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @is_owner()
    async def updateeco(self,ctx):
        db = await sql.connect('economy.db')
        await db.execute("CREATE TABLE IF NOT EXISTS economy (id not null primary key, user text, coins integer)")
        await db.commit()
        await ctx.send("reloaded economy.")




    async def add_coins(self, user: discord.Member, coins: int):
        db = await sql.connect('economy.db')
        user = str(user.id)
        existing_coins = await db.execute_fetchall("SELECT coins, id FROM economy WHERE user=?", [user])
        if not existing_coins:
            print(" if happens")
            existing_coins = 0
            ididid = 1
        elif existing_coins != None:
            idid = existing_coins[0][1]
            existing_coins = existing_coins[0][0]
            ididid = idid
        new_coins = existing_coins + coins
        params = [ididid,user,new_coins]
        await db.execute("INSERT or REPLACE INTO economy VALUES (?,?,?)", params) 
        await db.commit()
        return "200"

    async def subtract_coins(self, user: discord.Member, coins: int):
        db = await sql.connect('economy.db')
        user = str(user.id)
        existing_coins = await db.execute_fetchall("SELECT coins, id FROM economy WHERE user=?", [user])
        if not existing_coins:
            print(" if happens")
            existing_coins = 0
            ididid = 1
        elif existing_coins != None:
            idid = existing_coins[0][1]
            existing_coins = existing_coins[0][0]
            ididid = idid

        if existing_coins < 0:
            existing_coins = 0
        new_coins = existing_coins - coins
        if new_coins < 0:
            new_coins = 0
        params = [ididid,user,new_coins]
        await db.execute("INSERT or REPLACE INTO economy VALUES (?,?,?)", params) 
        await db.commit()
        return "200"

    async def get_bal_embed(self, user: discord.Member):
        db = await sql.connect('economy.db')
        useridid = str(user.id)
        coins = await db.execute_fetchall("SELECT coins FROM economy WHERE user=?", [useridid])
        print(coins)

        try:
            coins[0][0]
        except:
            coins = 0

        time = datetime.datetime.utcnow()
        em = discord.Embed(title=f"{user.display_name}'s balance", description=f"**Balance**: ⏣ {coins[0][0]} ", color=discord.Colour.green(), timestamp=time)
        em.set_footer(text="try fishing or coinflip to make coins easily!")
        em.set_thumbnail(url=user.avatar_url)
        return em

    async def get_bal(self, user: discord.Member):
        db = await sql.connect('economy.db')
        useridid = str(user.id)
        coins = await db.execute_fetchall("SELECT coins FROM economy WHERE user=?", [useridid])
        print(coins)        
        return coins[0][0]


    @commands.command(aliases=["bal", "money"])
    async def balance(self, ctx, user: discord.Member=None):
        user = ctx.author
        
        if not user:
            user = user

        em = await self.get_bal_embed(user)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 86400, type=BucketType.user)
    async def daily(self, ctx):
        user = ctx.author
        result = await self.add_coins(user,1000)
        if result == "200":
            em = await self.get_bal_embed(user)
            await ctx.send(embed=em)

    @daily.error
    async def on_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cmd = ctx.command
            cooldown = cmd.get_cooldown_retry_after(ctx)
            cooldown = round(cooldown)
            hours = time.gmtime(cooldown)
            hours = time.strftime("%H", hours)
            await ctx.send(f"You already used the daily command! Come back in **{hours}** hours.")

    @commands.command(aliases=["flip"])
    async def coinflip(self, ctx, coins: int=None,*, picked: str=None):
        if not coins:
            await ctx.send("you forgot to provide how much coins you wanna bet, eg. `-flip 2000 tails`")
            return

        if not picked:
            await ctx.send("the parameter should be something like `t/tails/h/heads`, eg. `-flip 200 h`")
            return

        if picked.lower() == "h":
            picked = "heads"
        elif picked.lower() == "t":
            picked = "tails"
        elif picked.lower() == "heads":
            picked = "heads"
        elif picked.lower() == "tails":
            picked = "tails"
        else:
            await ctx.send("the parameter should be something like `t/tails/h/heads`, eg. `-flip 200 h`")
            return
            


        p = ["heads", "tails"]

        pdone = random.choice(p)
        if pdone == picked:
            result = await self.add_coins(ctx.author, coins)
            if result == "200":
                em = discord.Embed(title=f"you were right! it was {pdone}!", description=f"You have earned ⏣ {coins}.",color=discord.Colour.green())
                await ctx.send(embed=em)
                return

        if pdone != picked:
            result = await self.subtract_coins(ctx.author, coins)
            if result == "200":
                em = discord.Embed(title=f"you were wrong... it was {pdone} :\\", description=f"You lost ⏣ {coins}.",color=discord.Colour.green())
                await ctx.send(embed=em)


    @commands.command()
    @commands.cooldown(1, 8, type=BucketType.user)
    async def fish(self, ctx):
        msg = await ctx.send("You are fishing <:fishing:837678036488552459>...")
        await asyncio.sleep(random.randint(0, 5))
        choices = ["good", "shark", "shoe", "mermaid", "merman"]
        choosing = random.choice(choices)

        if choosing == "good":
            coins = random.randint(1, 500)
            result = await self.add_coins(ctx.author, coins)
            if result == "200":
                await msg.edit(content=f"you found ⏣ **{coins}** from the sea! somehow..")

        elif choosing == "shark":
            coins = random.randint(1, 300)
            result = await self.subtract_coins(ctx.author, coins)
            if result == "200":
                await msg.edit(content=f"you found an ugly shark :shark: which attacked you, you lost ⏣ **{coins}**, rip.")
        elif choosing == "shoe":
            pchoices = ["coins", "snake", "nothing"]
            pchoosing = random.choice(pchoices)
            if pchoosing == "coins":
                coins = random.randint(1, 50)
                result = await self.add_coins(ctx.author, coins)
                if result == "200":
                    await msg.edit(content=f"You found a shoe which had ⏣ **{coins}** inside it. You kept the coins and threw away the shoe.")
            elif pchoosing == "snake":
                coins = random.randint(1, 200)
                result = await self.subtract_coins(ctx.author, coins)
                if result == "200":
                    await msg.edit(content=f"You found a shoe which had a snake inside it. The snake attacked you and you lost ⏣ **{coins}**.")
            elif pchoosing == "nothing":
                await msg.edit(content=f"You found a shoe which had... nothing inside. Lol sucks to suck")

        elif choosing == "mermaid":
            pchoices = ["good", "bad", "rare"]
            pchoosing = random.choice(pchoices)
            if pchoosing == "good":
                coins = random.randint(1, 500)
                res = await self.add_coins(ctx.author, coins)
                if res == "200":
                    await msg.edit(content=f"You found a mermaid which gave you c **{coins}** cuz why not.")
            if pchoosing == "bad":
                coins = random.randint(1, 1000)
                res = await self.subtract_coins(ctx.author, coins)
                if res == "200":
                    await msg.edit(content=f"You found a mermaid and had sex with it. You got arrested for beastiality and paid a ⏣ **{coins}** fine.")
        elif choosing == "merman":
            coins = random.randint(1, 5000)
            res = await self.subtract_coins(ctx.author, coins)
            if res == "200":
                await msg.edit(content=f"You found a merman which stole ⏣ **{coins}** from you. He swam away.")




    @fish.error
    async def on_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cmd = ctx.command
            cooldown = cmd.get_cooldown_retry_after(ctx)
            cooldown = round(cooldown)
            await ctx.send(f"wait **{cooldown}** seconds before you can use the command again!")

    @commands.command()
    @commands.cooldown(1,10, type=BucketType.user)
    async def work(self, ctx):
        coins = random.randint(1, 1500)
        works = [f"you worked at Taco Bell and got ⏣ {coins}.", f"you starting working at a strip club and gave Elon Musk a lap dance. You got ⏣ {coins} from the generous man.", f"You hacked NASA and extorted ⏣ {coins}", f"you won a dance contest doing the scrubs poison dance. You got ⏣ {coins}.", f"You defeated eminem in a rap battle and got ⏣ {coins}", f"You taught kim jong how to DM egirls. You got {coins}, damn.", f"You begged. You got ⏣ {coins} from busy bussinessmen", f"You became a cam femboy and earned ⏣ {coins}", f"You taught kids swear words. They paid you ⏣ {coins}.", f"You worked as an angry janitor in a hospital. You earned ⏣ {coins}."]

        job = random.choice(works)
        res = await self.add_coins(ctx.author, coins)
        if res == "200":
            time = datetime.datetime.utcnow()
            em = discord.Embed(description=job, color=discord.Colour.green(), timestamp=time)
            em.set_footer(text="check out other commands!")
            await ctx.send(embed=em)

    @work.error
    async def on_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cmd = ctx.command
            cooldown = cmd.get_cooldown_retry_after(ctx)
            cooldown = round(cooldown)
            await ctx.send(f"wait **{cooldown}** seconds before you can use the command again!")

    @commands.command()
    async def slut(self, ctx):
        pass

    @commands.command()
    async def drop(self, ctx,*, coins: int):
        user = ctx.author
        db = await sql.connect('economy.db')
        useridid = str(user.id)
        bal = await db.execute_fetchall("SELECT coins FROM economy WHERE user=?", [useridid])
        bal = bal[0][0]
        if coins > bal:
            await ctx.send("You dont have that much money to drop! Check your balance.")
            return


        em = discord.Embed(description=f"Quick! {user.mention} just dropped ⏣ {coins} ! pick it up using `-pick`", color=discord.Colour.green())
        await ctx.send(embed=em)
        await ctx.message.delete()

        def check(m):
            return m.content.lower() == "-pick"

        msg = await self.bot.wait_for("message", timeout=60.0, check=check)
        userpicked = msg.author
        res = await self.add_coins(userpicked, coins)
        res1 = await self.subtract_coins(user, coins)
        if res == "200" and res1 == "200":
            em = discord.Embed(description=f"{userpicked} picked up ⏣ {coins}! check balance using `-bal`", color=discord.Colour.green())
            await ctx.send(embed=em)

        










    



def setup(bot):
	bot.add_cog(Economy(bot))