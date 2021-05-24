import discord
from discord.ext import commands
import asyncio
import time
import requests
import json
import random
import os
import asyncpraw
import TenGiphPy
import database as dbpy
from throwbin import ThrowBin
import textwrap
import helpinfo as hi
from google_trans_new import google_translator  
import subprocess
import aiohttp
import asyncdagpi
import socid_extractor
from asyncdagpi import ImageFeatures 
from pornhub_api import PornhubApi
from bs4 import BeautifulSoup
import datetime
import re
from TwitterAPI import TwitterAPI
import matplotlib.pyplot as plt
import analysis
import numpy as np
import jishaku
from PIL import Image
from PIL import ImageOps
from PIL import ImageFont
from PIL import ImageDraw
import urllib.request
import aiosqlite
from fake_useragent import UserAgent

'''
as you can see, i've hard coded most of my commands here because i was a dumbass child coding on discord.py for the first time. I'd turn it into cogs if it were'nt for the number of bugs i dont wanna deal with since i've moved on to new projects.

if you can  turn these into cogs i'd say thanks, just make a pull request! 

'''

ua = UserAgent()
ua.update()


phub = PornhubApi()

dagpi = asyncdagpi.Client("") # DAGPI token, dagpi.xyz

translator = google_translator()  

tb = ThrowBin()


clr = [discord.Color.dark_orange(),discord.Color.orange(),discord.Color.dark_gold(),discord.Color.gold(),discord.Color.dark_magenta(),discord.Color.magenta(),discord.Color.red(),discord.Color.dark_red(),discord.Color.blue(),discord.Color.dark_blue(),discord.Color.teal(),discord.Color.dark_teal(),discord.Color.green(),discord.Color.dark_green(),discord.Color.purple(),discord.Color.dark_purple()]

pid = os.getpid()

TOKEN = "" # discord bot token

g = TenGiphPy.Giphy(token='') # Giphy token

# reddit credentials.

r_client_id = ""
r_client_secret = ""
r_pass = ""
r_username = ""

reddit = asyncpraw.Reddit(client_id=r_client_id,client_secret=r_client_secret,user_agent='add a nice useragent string here', username	=r_username, password=r_pass)

# twitter credentials. Yes, i let a bunch of people post tweets anytime using my bot.

access_token = ""
access_secret = ""
consumer_key = ""
consumer_secret = ""

intents = discord.Intents.default()
intents.members = True


bot = commands.AutoShardedBot(command_prefix=[",","++"],description="The one and only, golds.", intents=intents, case_insensitive=True)



bot.remove_command('help')

bot.load_extension('jishaku')

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extenstion}')
    
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
blist = []


@bot.command(pass_context=True)
async def horny(ctx, *, sent):
  sent = str(sent)
  sentences = [sent]
  sent = sentences[-1]
  ranger = random.randint(1, 10)
  for x in range(ranger):
    words = sent.split()
    word = random.choice(words)
    replaced = sent.replace(word, "horny")
    sentences.append(replaced)
    
  await ctx.reply(sentences[-1])

async def search_members(query, guild: discord.Guild):
	results = []
	for member in guild.members:
		if query in member.name.lower() or query in member.display_name.lower():
			results.append(f"<@!{member.id}>")
	return results
	
@bot.command(pass_context=True)
async def query(ctx,*,query):
	query = str(query)
	try:
		guild = ctx.guild
		
	except:
		await ctx.send("You cant run this command in DMs")
		
	results = await search_members(query,ctx.guild)
	resultcount = len(results)
	if len(results) == 0:
		time = datetime.datetime.utcnow()
		em = discord.Embed(title=f"members named {query}", description="No users found.", color=discord.Colour.magenta(), timestamp=time)
		em.set_thumbnail(url=ctx.guild.icon_url)
		em.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
		em.set_footer(text="check out other commands with ,help")
		await ctx.send(embed=em)
		return
	results = "\n".join(results)
	time = datetime.datetime.utcnow()
	em = discord.Embed(title=f"members named {query}", description=results, color=discord.Colour.magenta(), timestamp=time)
	em.set_thumbnail(url=ctx.guild.icon_url)
	em.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
	em.set_footer(text=f"found {resultcount} out of {len(ctx.guild.members)} members.")
	await ctx.send(embed=em) 
	
async def getUnscramble(word):
	url = f"https://unscramblex.com/anagram/{word}"
	res = requests.get(url)
	sp = BeautifulSoup(res.text)
	words_ = sp.find_all('span',class_="words__textInner")
	words = []
	for word in words_:
		word = str(word.text)
		words.append(word)
		if len(word) == 2:
			words.remove(word)
		
	return words
	
@bot.command(pass_context=True, aliases=["uns"])
async def unscramble(ctx,*,word):
	word = str(word)
	words = await getUnscramble(word)
	desc = "\n".join(words)
	time = datetime.datetime.utcnow()
	embeduns = discord.Embed(title=f"{word} unscrambled", description=desc, color=discord.Colour.magenta(), timestamp=time)
	embeduns.set_footer(text="loool")
	await ctx.send(embed=embeduns)
	
	
	
	

@bot.command(pass_context=True)
@commands.is_owner()
async def updatedb(ctx):
	db = await aiosqlite.connect('./db/dadatabase.db')
	await ctx.send("updated databases.")
	await db.close()
	file = discord.File('./db/dadatabase.db')
	await ctx.author.send(file=file)

@bot.command(pass_context=True)
async def todo(ctx,mode=None,*,doing=None):
	
	db = await aiosqlite.connect('./db/dadatabase.db')

	if not mode:
		tablename = f"todosof{ctx.author.id}"
		try:
			alltasks = await db.execute("SELECT * FROM "+ tablename)
			
		except:
			await ctx.send("usage:\n`,todo add`\n`,todo done [task number]`")
			return
			
		alltasks = await alltasks.fetchall()
		forembed = []
		for task in alltasks:
			task1 = f"`[{task[0]}]` **{task[1]}**"
			forembed.append(task1)
			
		toembed = "\n".join(forembed)
		embed = discord.Embed(title="todo",description=toembed)
		embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
		embed.set_thumbnail(url=ctx.author.avatar_url)
		await ctx.send(embed=embed)
		await db.close()
		return
		
	if mode.lower() == "add" and doing != None:
		tablename = f"todosof{ctx.author.id}"
		
		cursor = await db.execute("CREATE TABLE IF NOT EXISTS " + tablename +" (taskid not null primary key, doing text)")
		await db.commit()
		
		
		
		try:
			cursor = await db.execute("SELECT * FROM " + tablename +" WHERE taskid=(SELECT max(taskid) FROM "+ tablename +")")
			cursor = await cursor.fetchone()
			id = cursor[0]
			id = id + 1
			
		except:
			id = 1
			
		params = [id, doing]
		
		cursor = await db.execute("INSERT INTO "+ tablename +" VALUES (?, ?)", params)
		
		await db.commit()
		
		alltasks = await db.execute(f"SELECT * FROM {tablename}")
		alltasks = await alltasks.fetchall()
		
		forembed = []
		for task in alltasks:
			task1 = f"`[{task[0]}]` **{task[1]}**"
			forembed.append(task1)
			
		toembed = "\n".join(forembed)
		embed = discord.Embed(title="todo",description=toembed)
		embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
		embed.set_thumbnail(url=ctx.author.avatar_url)
		await ctx.send(embed=embed)
		await db.close()
		
	if mode.lower() == "done":
		try:
			doing = int(doing)
			
		except:
			await ctx.send("please provide a valid task number, do `,todo` to check your tasks.")
			return
			
		tablename = f"todosof{ctx.author.id}"
		cursor = await db.execute("DELETE FROM "+ tablename + f" WHERE taskid={doing}")
		await db.commit()
		embed=discord.Embed(description="task completed! Do `,todo` to check your tasks")
		await ctx.send(embed=embed)
		await db.close()
		
			
			
		
		
async def getAnimeTorrents(anime):
	url = f"https://nyaa.si/?q={anime}&f=0&c=0_0"
	
	res = requests.get(url)
	sp = BeautifulSoup(res.text)
	
	titles = []
	torlinks = []
	
	tables = sp.find_all('td', {'colspan': '2'})
	for table in tables:
		try:
			tablesoup = BeautifulSoup(str(table))
			title = tablesoup.find('a')
			title = title['title']
			titles.append(str(title))
			
		except:
			pass
			
		links = sp.find_all('td', class_="text-center")
		for link in links:
			try:
				tablelink = BeautifulSoup(str(link))
				link = tablelink.find('a')
				link = link['href']
				torlinks.append(f"https://nyaa.si{link}")
				
			except:
				pass
				
		forembed = []
		
		for title,link in zip(titles,torlinks):
					if "comment" in title:
						continue
					else:
						forembed.append(f"[{title}]({link})")
		
		toembed = []
					
		for x in range(8):
				toembed.append(forembed[x])
				
		
				
		return toembed
		
		
@bot.command(pass_context=True)
async def animetorrents(ctx,*,anime=None):
				if not anime:
					await ctx.send("you didnt mention the anime you want the torrents for.\nusage: `,animetorrents jojo golden wind 38`")
					return
				results = await getAnimeTorrents(anime)
				
				forembed = "\n".join(results)
				embed = discord.Embed(description=forembed)
				embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar_url)
				embed.set_footer(text="powered by goldys huge cock again")
				await ctx.send(embed=embed)
				
		
		
	
async def makeDisco():
	im = Image.open('./image_cache/fordisco.png').convert('RGBA')
	colors = ['#BB19BB','#BB19BB','#BB19BB', '#862567','#862567','#862567', '#47B4B1','#47B4B1','#47B4B1', '#E6E12C', '#E6E12C', '#E6E12C', '#30057C', '#30057C', '#30057C']
	images = []
	num = 0
	for color in colors:
		num += 1
		im.load()
		r, g, b, alpha = im.split()
		gray = ImageOps.grayscale(im)
		result = ImageOps.colorize(gray, (0, 0, 0, 0), color)
		result.putalpha(alpha)
		tinted = result 
		tinted.save(f'./image_cache/gifcache{num}.png')
		img = Image.open(f'./image_cache/gifcache{num}.png')
		images.append(img)
		
	images[0].save('./image_cache/disco.gif', save_all=True, append_images=images[1:], optimize=False, duration=40, loop=0)
	file = discord.File('./image_cache/disco.gif', spoiler=True)
	lencolors = len(colors) + 1
	for x in range(lencolors):
		try:
			os.remove('./image_cache/gifcache{x}.png')
		except:
			pass
	print("cleared gif cache")
	
	return file
	
@bot.command(pass_context=True)
async def disco(ctx, member: discord.User=None):
			if member == None:
				pass
			if member != None:
				url = member.avatar_url_as(format="png", size=1024)
				urllib.request.urlretrieve(url, "./image_cache/fordisco.png")
				async with ctx.channel.typing():
					msg = await ctx.send('processing...')
					attach = ctx.message.attachments[0]
					await attach.save('./image_cache/fordisco.png')
					file = await makeDisco()
					await msg.delete()
					await ctx.send("warning: flashing colors",file=file)
				os.remove('./image_cache/disco.gif')
				return
				
			if not ctx.message.attachments:
				await ctx.send("you didnt send an image with the command to disco\nusage ```,disco [image] ```")
			elif ctx.message.attachments:
				async with ctx.channel.typing():
					msg = await ctx.send('processing...')
					attach = ctx.message.attachments[0]
					await attach.save('./image_cache/fordisco.png')
					file = await makeDisco()
					await msg.delete()
					await ctx.send("warning: flashing colors",file=file)
			try:
				os.remove('./image_cache/disco.gif')
			except:
				print("no disco.gif found.")
		
		
	
async def generatefb(text):
	if len(text) >= 15:
		texts = textwrap.wrap(text, width=25)
		text = "\n".join(texts)
		font = ImageFont.truetype('./fonts/roboto.ttf', 69)
		img = Image.open('facebook.jpg')
		draw = ImageDraw.Draw(img)
		draw.text((239,227), f"{text}", (0,0,0), font=font)
		img.save('./image_cache/facebook.jpg')
		file = discord.File('./image_cache/facebook.jpg')
		return file
		
	font = ImageFont.truetype('./fonts/roboto.ttf', 69)
	img = Image.open('facebook.jpg')
	draw = ImageDraw.Draw(img)
	draw.text((359,385), f"{text}", (0,0,0), font=font)
	img.save('./image_cache/facebook.jpg')
	file = discord.File('./image_cache/facebook.jpg')
	return file
	
@bot.command(pass_context=True)
@commands.cooldown(1,3)
async def facebook(ctx,*,text):
	text = str(text)
	file = await generatefb(text)
	await ctx.send(file=file)
	os.remove('./image_cache/facebook.jpg')
	
	
async def tintimage():	
		src = Image.open('./image_cache/unedited.png').convert('RGBA')
		color = "#%06x" % random.randint(0, 0xFFFFFF)
		src.load()
		r, g, b, alpha = src.split()
		gray = ImageOps.grayscale(src)
		result = ImageOps.colorize(gray, (0, 0, 0, 0), color)
		result.putalpha(alpha)
		
		tinted = result 
		tinted.save('./image_cache/tinted.png')
		file = discord.File('./image_cache/tinted.png')
		os.remove('./image_cache/unedited.png')
		return file
		
		
@bot.command(pass_context=True)
async def tint(ctx):
		if not ctx.message.attachments:
			await ctx.send("you didnt send an image with the command to tint\nusage ```,tint [image] ```")
		elif ctx.message.attachments:
			msg = await ctx.send('processing...')
			attach = ctx.message.attachments[0]
			await attach.save('./image_cache/unedited.png')
			file = await tintimage()
			await msg.delete()
			await ctx.send(file=file)
			os.remove('./image_cache/tinted.png')
			
		
		
@bot.command(pass_context=True)
@commands.is_owner()
async def scrape(ctx,guild,channel):
	guild = bot.get_guild(int(guild))
	meguild = bot.get_guild(810359062079471637)
	channel = guild.get_channel(int(channel))
	tochannel = meguild.get_channel(823409046878552064)
	async for message in channel.history():
		if message.attachments:
			for attachment in message.attachments:
				await tochannel.send(attachment.url)
				
	

@bot.command(pass_context=True)
async def getTitles():
	num = random.randrange(1,69)
	url = f"https://www.xvideos.com/new/{num}"
	res = requests.get(url)
	sp = BeautifulSoup(res.text)
	atags = sp.find_all("a")
	titles = []
	for tag in atags:
		try:
			if len(tag['title']) > 14:
				titles.append(tag['title'])
		except:
				pass
	return titles
	
@bot.command(pass_context=True, aliases=["pt"])
async def porntitle(ctx):
				if not ctx.channel.is_nsfw():
					await ctx.send("not an NSFW channel!")
					return
				titles = await getTitles()
				title = random.choice(titles)
				await ctx.send(f"{title}")
				

async def getBingImages(query):
	url = f"https://www.bing.com/images/search?q={query}"
	res = requests.get(url)
	sp = BeautifulSoup(res.text)
	links = []
	atags = sp.find_all('a')
	for tag in atags:
		try:
			dic = str(tag['m'])
			dic = json.loads(dic)
			link = str(dic["murl"])
			links.append(link)
			
		except:
			pass
	return links
	

lastuser = []
lastmsg = []	

@bot.command(pass_context=True, aliases=["im", "image"])
async def img(ctx,*,query):
	lastuser.insert(0,ctx.author.id)
	query = str(query)
	links = await getBingImages(query)
	embed = discord.Embed(title="your image search results..", url="https://bing.com", description="type \"n\" for the next image.")
	def randlink():
		link = random.choice(links)
		links.remove(link)
		return link
		
	linknum = len(links)
		
	pagenum = {'num': 1}
	pagenumber = pagenum['num']
		
	embed.set_image(url=randlink())
	embed.set_footer(text=f"page {pagenumber}/{linknum}")
	msg = await ctx.send(embed=embed)
	lastmsg.insert(0,msg.id)
	
	msgfordelete = []
	
	def check(m):
		if "n" in m.content and m.author == ctx.author:
			if lastuser[0] == m.author.id:
				msgd = m.channel.get_partial_message(lastmsg[0])
				msgfordelete.append(msgd)
				return True
			else:
				return True
				
	try:
			msgd = msgfordelete[0]
			await msgd.delete()
	except:
			pass
			
			
	end = time.time() + 25
	while time.time() < end:
							msg2 = await bot.wait_for('message', timeout=20.0, check=check)
							await msg2.delete()
							embed.set_image(url=randlink())
							pagenumber += 1
							toupdate = {'num': pagenumber}
							pagenum.update(toupdate)
							embed.set_footer(text=f"page {pagenumber}/{linknum}")
							await msg.edit(embed=embed)	
	
@img.error
async def img_error(ctx, error):
	return
	

	
@bot.command(pass_context=True)
async def analyze(ctx):
	msg = ctx.message.reference.resolved
	content = str(msg.content)
	scores = analysis.getTheScore(content)
	horny = scores['flirt']
	toxic = scores['toxic']
	await ctx.send(f"message: \" {content}\"\n\n horny: `{horny}/10`\n toxic: `{toxic}/10`")

	
	
	
async def getWordData(ctx,word):
	word = str(word)
	word = word.lower()
	profile = {}
	async for message in ctx.channel.history(limit=5000):
		content = message.content.lower()
		if word in content:
					try:
						author = profile[message.author.display_name]
						profile[message.author.display_name] += 1				
					except:
						profile[message.author.display_name] = 0
						profile[message.author.display_name] += 1
	return profile
	
async def plotchart(word, profile):
	authors = list(profile.keys())
	values = list(profile.values())			
	
	fig = plt.figure(figsize = (12, 9))
	# create bar
	plt.bar(authors, values, color = '#FF67DF', width = 0.5)
	plt.xlabel(f"users who've said the word {word}")
	plt.ylabel(f"No. of times they've said {word}")
	plt.title(f"number of times people have said {word}")
	plt.savefig('./image_cache/chart.png')
	print("saved chart")
	file = discord.File('./image_cache/chart.png')
	print("discord.File success")
	return file
	
	
	
@bot.command(pass_context=True)
@commands.cooldown(1,60)
async def stats(ctx,*,word):
	now = time.time()
	word = str(word)
	msg = await ctx.send("this might take a long while...<a:golds_loading:821343936232554536>")
	profile = await getWordData(ctx,word)
	chart = await plotchart(word, profile)
	then = time.time()
	lat = then - now
	lat = round(lat)
	await ctx.send(f"`{lat}` seconds",file=chart)
	await msg.delete()
	os.remove('./image_cache/chart.png')
	
	
	
@bot.command(pass_context=True)
async def kanye(ctx):
	res = requests.get("https://api.kanye.rest/")
	res = res.json()
	quote = res["quote"]
	embed = discord.Embed(description=f"{quote} -- Kanye West")
	embed.set_footer(text="random kanye west quote")
	await ctx.send(embed=embed)
async def redgifs(url):
	res = requests.get(url)
	soup = BeautifulSoup(res.text)
	gif = soup.find('img', class_="gif")
	gif = gif["src"]
	return str(gif)
	
async def getword():
	res = requests.get("https://www.vocabulary.com/dictionary/randomword")
	soup = BeautifulSoup(res.text)
	area = soup.find('div', class_="word-area")
	wordarea = BeautifulSoup(str(area))
	long = wordarea.find('p', class_="long")
	long = long.text
	short = wordarea.find('p', class_="short")
	short = short.text
	word = wordarea.find('h1')
	word = word.text
	randword = {}
	randword["word"] = str(word)
	randword["long"] = str(long)
	randword["short"] = str(short)
	return randword
	
@bot.command(pass_context=True, aliases=["random"])
async def _random(ctx):
	word = await getword()
	long = word["long"]
	short = word["short"]
	worded = word["word"]
	embed = discord.Embed(title=worded, description=f"{short}\n \n{long}\n \n", color=0x373BFF)
	embed.set_footer(text="📖 | powered by vocabulary.com")
	await ctx.send(embed=embed)
			
	
@bot.command(pass_context=True)
async def blacklist(ctx,*,user: discord.Member):
        	
        	blist.append(user.id)
        	        	
        
@bot.command(pass_context=True, aliases=["aswin"])
async def goldy(ctx):
	await ctx.send("https://cdn.discordapp.com/attachments/787849647753265213/819492473117474836/badameez_dil_SD_360p.mp4")
	
async def getcheese(cheese):
	url = f"https://cheese.com/?q={cheese}"
	res = requests.get(url)
	soup = BeautifulSoup(res.text)
	div = str(soup.find('div', class_="catalog search-results internal"))
	soup2 = BeautifulSoup(div)
	getlink = soup2.find('a')
	link = f"https://cheese.com{getlink['href']}"
	getimg = soup2.find('img')
	img = f"https://cheese.com{getimg['src']}"
	result = {}
	result["link"] = link
	result["image"] = img
	return result
	
	
@bot.command(pass_context=True)
async def cheese(ctx,*,cheese=None):
	if cheese == None:
		await ctx.send("usage: `,cheese cottage cheese`")
		return
		
	cheese = str(cheese)
	result = await getcheese(cheese)
	link = result["link"]
	image = result["image"]
	embed = discord.Embed(title=cheese, url=link,color=0xF6D85F)
	embed.set_image(url=image)
	embed.set_footer(text=" 🧀 | powered by cheese.com")
	await ctx.send(embed=embed)
	
	
async def searchtwitter(query):
	api = TwitterAPI(consumer_key,consumer_secret, access_token, access_secret)
	r = api.request('search/tweets', {'q': 'boobs'})
	rawtweets = []
	for item in r.get_iterator():
		if "text" in item:
			rawtweets.append(item)
					
		elif 'message' in item and item['code'] == 88:
			pass
			
		tweets = []
		tweets.append(rawtweets[0])
		tweets.append(rawtweets[1])
		tweets.append(rawtweets[2])
		tweets.append(rawtweets[3])
		tweets.append(rawtweets[4])
			
			
		return tweets
								
				
@bot.command(pass_context=True, aliases=["twt"])
async def twitter(ctx,*,query):
			if ctx.author.id == any(blist):
				await ctx.send("ur blacklisted dumb hoe")
				return
			query = str(query)
			items = await searchtwitter(query)
			for item in items:
				user = item['user']['name']
				text = item['text']
				timestamp = item['timestamp_ms']
				followers = item['user']['followers_count']
				avatar = item['user']['profile_image_url_https']
				replies = item['reply_count']
				retweets = item['retweet_count']
				embed = discord.Embed(description=text, color=0xFFFFFF)
				embed.set_author(name=f"user ( {followers} followers)", icon_url=avatar)
				embed.set_footer(text=f" {replies} replies | {retweets} retweets")
				await ctx.send(embed=embed)
			
	

async def postit(ctx,tweet, author):
    TWEET_TEXT = f"{tweet}"
    
    if len(TWEET_TEXT) >= 280:
      await ctx.send("uh oh, thats above the word limit for Twitter")
      
    api = TwitterAPI(consumer_key,consumer_secret, access_token, access_secret)
    r = api.request('statuses/update', {'status': TWEET_TEXT})
    getlink = r.json()
    try:
    	link = getlink['id_str']
    	
    except:
    	await ctx.send(f"either twitter banned me or something went really wrong \n ```py \n {getlink} \n ```")
    	return
    link = getlink['id_str']
    link = f"https://twitter.com/goldyscock/status/{link}"
    return link
    
 
 
@bot.command(pass_context=True)
@commands.cooldown(1,10)
async def tweet(ctx,*,tweettext):
	tweettext = str(tweettext)
	author = ctx.author.display_name
	post = await postit(ctx,tweettext, author)
	await ctx.send(post)
	
	
async def getinsta(username):
	url = f"https://privatephotoviewer.com/profile/{username}"
	headers = {'User-agent': "goldsy lool"}
	res = requests.get(url, headers)
	sp = BeautifulSoup(res.text)
	profile = {}
	
	followers = sp.find('span', class_='followerCount')
	followers = followers.text
	
	following = sp.find('span', {'id': 'following'})
	following = following.text
	
	username = sp.find('span', {'id': 'username'})
	username = username.text
	
	bio = sp.find('p', {'id': 'biofull'})
	bio = bio.text
	
	name = sp.find('h1', {'id': 'userfullname'})
	name = name.text
	
	avatar = sp.find('img', class_='profile-img avatar user-image')
	avatar = avatar['src']
	
	posts = sp.find('span', {'id': 'posttoal'})
	posts = posts.text
	
	profile["avatar"] = str(avatar)
	profile["link"] = f"https://instagram.com/{username}"
	profile["name"] = str(name)
	profile["bio"] = str(bio)
	profile["followers"] = str(followers)
	profile["following"] = str(following)
	profile["posts"] = str(posts)
	return profile
	
	
	

	
@bot.command(pass_context=True,aliases=["insta"])
async def instagram(ctx,*,username):
	username = username.lower()
	profile = await getinsta(username)
	avatar = profile["avatar"]
	link = profile["link"]
	name = profile["name"]
	bio = profile["bio"]
	followers = profile["followers"]
	following = profile["following"]
	posts = profile["posts"]
	
	embed = discord.Embed(title=name,url=link, color=0x8807FD)
	embed.add_field(name="followers", value=followers, inline=False)
	embed.add_field(name="following", value=following, inline=False)
	embed.add_field(name="bio", value=bio, inline=False)
	embed.add_field(name="posts", value=posts, inline=False)
	
	embed.set_thumbnail(url=avatar)
	embed.set_footer(text="powered by goldys huge cock")
	await ctx.send(embed=embed)
	
	
async def gettumblr(query):
        url = f"https://www.tumblr.com/search/{query}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text)
        links = []
        imgs = soup.find_all('img', attrs = {'srcset': True})
        for img in imgs:
        	links.append(str(img['srcset']))
        	
        return links

@bot.command(pass_context=True, aliases=["tbr"])    
async def tumblr(ctx,*,query):
        query = str(query)
        links = await gettumblr(query)
        link = random.choice(links)
        link2 = re.findall(r'(https?://[^\s]+)', link)
        num = len(link) - 1
        link = link2[num]
        
        await ctx.send(f"{link}")
        
@bot.command(pass_context=True)
async def susu(ctx):
	await ctx.send("https://cdn.discordapp.com/attachments/672436233229828108/817766306106835014/challo.mp4")
async def gethoroscope(sign):
	url = f"https://www.astrology.com/horoscope/daily/{sign}.html"
	response = requests.get(url)
	soup = BeautifulSoup(response.text)
	divs = soup.find_all('div', class_="grid-md-c-s2")
	soup2 = BeautifulSoup(str(divs))
	body = soup2.find_all('p')
	soup3 = BeautifulSoup(str(body))
	text = soup3.text
	content = text[3:-1]
	return str(content)
	
	
@bot.command(pass_context=True)
async def horoscope(ctx,*,sign):
	sign = str(sign)
	sign = sign.lower()
	emojis = dbpy.signs
	emote = emojis[f"{sign}"]		
	scope = await gethoroscope(sign)
	day = datetime.datetime.today().weekday()
		
	embed = discord.Embed(title=f"{emote} {sign} {emote}", description=f"\n {scope} \n", color=0x74009E)
	embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/672436233229828108/817705749404450826/IMG_20210306_155119.jpg")
	embed.set_footer(text=f"{emote} | powered by astrology.com")
	await ctx.send(embed=embed)		
		
async def getwhi(query):
	url = f"https://weheartit.com/search/entries?query={query}"
	r = requests.get(url)
	soup = BeautifulSoup(r.content)
	divs = str(soup.find_all('div', class_='entry grid-item'))
	soup2 = BeautifulSoup(divs)
	images = soup2.find_all('img')
	links = []
	for image in images:
		if "data.whicdn.com/images/" in str(image):
			links.append(image['src'])
			
	return links
			
	
@bot.command(pass_context=True, aliases=["whi", "aes"])
@commands.cooldown(1,15)
async def whoheartit(ctx,*,query):
		
		links = await getwhi(query)
		
		def randlink():
			link = random.choice(links)
			links.remove(link)
			return str(link)
			
		embed = discord.Embed(color=discord.Colour.magenta())
		embed.set_image(url=randlink())
		embed.set_footer(text="type 'n' for the next image.")
		msg = await ctx.send(embed=embed)
		
		def check(m):
							return m.content == 'n' and m.channel == ctx.channel
							
		t_end = time.time() + 20
		while time.time() < t_end:
							msg2 = await bot.wait_for('message', timeout=20.0, check=check)
							await msg2.delete()	
		embed0 = discord.Embed(color=discord.Colour.magenta())
		embed0.set_image(url=randlink())
		embed0.set_footer(text="type 'n' for the next image.")
		await msg.edit(embed=embed0)
	
        
@bot.command(pass_context=True)
async def pixel(ctx):
    if ctx.message.mentions:
    	member = ctx.message.mentions[0]
    	url = str(member.avatar_url_as(format="png", static_format="png", size=1024))
    	img = await dagpi.image_process(ImageFeatures.pixel(), url)
    	file = discord.File(fp=img.image,filename=f"pixel.{img.format}")
    	await ctx.send(file=file)
    	
    else:
    	member = ctx.author
    	url = str(member.avatar_url_as(format="png", static_format="png", size=1024))
    	img = await dagpi.image_process(ImageFeatures.pixel(), url)
    	file = discord.File(fp=img.image,filename=f"pixel.{img.format}")
    	await ctx.send(file=file)

		
@bot.command(pass_context=True, aliases=["alinaa", "leena"])
@commands.cooldown(1,10)
async def alina(ctx, *, love):
        	      			content = {}
        	      			content["guild"] = ctx.guild.id
        	      			content["author"] = ctx.author.id
        	      			content["channel"] = ctx.channel.id
        	      			content["love"] = love
        	      			love = str(content["love"])
        	      			if len(love) <= 15:
        	      				await ctx.send("make your letter longer hoe")
        	      				await ctx.message.delete()
        	      				
        	      			else:
        	      				await ctx.message.delete()
        	      				guild = bot.get_guild(int(content["guild"]))
        	      				channel = guild.get_channel(int(content["channel"]))
        	      				
        	      				user = guild.get_member(561329120068501514)
        	      				author = guild.get_member(int(content["author"]))
        	      				embed = discord.Embed(title="You have a love letter from {author} !", description=str(content["love"]), color=0xFF2E8C)
        	      				embed.set_thumbnail(url="https://icons.iconarchive.com/icons/webalys/kameleon.pics/256/Love-Letter-icon.png")
        	      				embed.set_footer(text=f"{ctx.guild}.")
        	      				await user.send(embed=embed)
        	      				author = guild.get_member(int(content["author"]))
        	      				embed1 = discord.Embed(description="Your love letter to alina been sent! ♡", color=0xFF2E8C)
        	      				embed1.set_footer(text="check out ,help for more commands <3")
        	      				embed1.set_author(name=author.display_name, icon_url=f"{author.avatar_url}")
        	      				embed1.set_thumbnail(url="https://cdn.discordapp.com/attachments/791837593448873994/812536859639939113/520_sin_titulo_20210219003742.png")
        	      				await channel.send(embed=embed1)	
    	

@bot.command(pass_context=True, aliases=["ph", "porn"])
@commands.cooldown(1,5)
async def pornhub(ctx,*, keyword=None):
    if keyword != None:
    		if ctx.channel.is_nsfw() == False:
    			await ctx.send("not an NSFW channel.")
    			return
    		data = phub.search.search(f"{keyword}",ordering="mostviewed",period="weekly")
    		results = []
    		for vid in data.videos:
    			results.append(vid.video_id)
    			if len(results) == 2:
    							for videoid in results:
    								await ctx.send(f"https://www.pornhub.com/view_video.php?viewkey={videoid}")
    								break
    						
    			
    		
    else:
    	await ctx.send("give me something to search for loser")
    
@bot.command(pass_context=True, aliases=["yt"])
async def youtube(ctx,*,query):
		      	async with aiohttp.ClientSession() as cs:
		      		async with cs.get(f'https://normal-api.ml/youtube/searchvideo?query={query}') as r:
		      			response = await r.text()
		      			res = json.loads(response)
		      			if res["status"] != "200":
		      				await ctx.send("can't find video #sad")
		      				return
		      				
		      			url = res["url"]
		      			await ctx.send(f"{url}")
		      			
@bot.command(pass_context=True)
async def panda(ctx):
		      	async with aiohttp.ClientSession() as cs:
		      		async with cs.get(f'https://some-random-api.ml/img/panda') as r:
		      			response = await r.text()
		      			res = json.loads(response)
		      			embed = discord.Embed(title="panda", color=discord.Colour.random())
		      			url = res["link"]
		      			embed.set_image(url=url)
		      			await ctx.send(embed=embed)
		      			
		      			
		      			
@bot.command(pass_context=True, aliases=["bird"])
async def birb(ctx):
		      	async with aiohttp.ClientSession() as cs:
		      		async with cs.get(f'https://some-random-api.ml/img/birb') as r:
		      			response = await r.text()
		      			res = json.loads(response)
		      			embed = discord.Embed(title="birb", color=discord.Colour.random())
		      			url = res["link"]
		      			embed.set_image(url=url)
		      			await ctx.send(embed=embed)
		      			
		      			
		      			
		      			
@bot.command(pass_context=True)
async def fox(ctx):
		      	async with aiohttp.ClientSession() as cs:
		      		async with cs.get(f'https://some-random-api.ml/img/fox') as r:
		      			response = await r.text()
		      			res = json.loads(response)
		      			embed = discord.Embed(title="fox", color=discord.Colour.random())
		      			url = res["link"]
		      			embed.set_image(url=url)
		      			await ctx.send(embed=embed)
		      			
		      			
@bot.command(pass_context=True)
async def coffee(ctx):
		      	async with aiohttp.ClientSession() as cs:
		      		async with cs.get(f'https://coffee.alexflipnote.dev/random.json') as r:
		      			response = await r.text()
		      			res = json.loads(response)
		      			embed = discord.Embed(title="coffee", color=discord.Colour.random())
		      			url = res["file"]
		      			embed.set_image(url=url)
		      			await ctx.send(embed=embed)		      			

		      			
@bot.command(pass_context=True, aliases=["ducks", "quack"])
async def duck(ctx):
		      	async with aiohttp.ClientSession() as cs:
		      		async with cs.get(f'https://random-d.uk/api/random') as r:
		      			response = await r.text()
		      			res = json.loads(response)
		      			embed = discord.Embed(title="duck", color=discord.Colour.random())
		      			url = res["url"]
		      			embed.set_image(url=url)
		      			await ctx.send(embed=embed)		      			
	
@bot.command(pass_context=True, aliases=['define', 'urban'])
async def df(ctx, *, dfword=None):
    if dfword != None:

        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

        querystring = {"term": f"{dfword}"}

        headers = {
            'x-rapidapi-key': "cba82f440bmshda4e373d225eb53p13a10bjsn820a70842220",
            'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
        }

        response = requests.request(
            "GET", url, headers=headers, params=querystring)

        dfdat = json.loads(response.text)
        df0 = dfdat["list"][0]

        definition = df0["definition"]
        word = df0["word"]
        example = df0["example"]
        thumbsup = df0["thumbs_up"]
        thumbsdown = df0["thumbs_down"]

        embed = discord.Embed(title=f"{word}",description=f"\n{definition} \n \n_{example}_ ")
        embed.set_footer(text=f"👍 {thumbsup} | 👎 {thumbsdown} ")
        await ctx.send(embed=embed)

    elif dfword == None:
        ctx.send("Gimme a word to find the definition for dummy.")
        
@bot.command(pass_context=True, aliases=['memes'])
async def meme(ctx):
    url = "https://meme-api.herokuapp.com/gimme"
    response = requests.request("GET", url)
    memedat = json.loads(response.text)
    postlink = memedat["postLink"]
    subreddit = memedat["subreddit"]
    title = memedat["title"]
    url = memedat["url"]

    embed = discord.Embed(
        title=f"{title}",
        url=f"{postlink}",
        color=random.choice(clr)
    )
    embed.set_footer(text=f"r/{subreddit}")
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def dog(ctx):
    url = "https://dog.ceo/api/breeds/image/random"

    response = requests.request("GET", url)
    dog = json.loads(response.text)
    image = dog["message"]

    embed = discord.Embed(
        title="dog",
        color=random.choice(clr)
    )
    embed.set_image(url=image)
    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def cat(ctx):
    url = "https://api.thecatapi.com/v1/images/search"

    response = requests.request("GET", url)
    cat = json.loads(response.text)
    image = cat[0]["url"]

    embed = discord.Embed(
        title="kitty :3",
        url=image,
        color=random.choice(clr)
    )
    embed.set_image(url=image)
    await ctx.send(embed=embed)	
		
@bot.command(pass_context=True, aliases=['q'])
async def quote(ctx):
	url = "https://api.quotable.io/random"
	response = requests.request("GET", url)
	q = json.loads(response.text)
	quote = q["content"]
	author = q["author"]
	embed = discord.Embed(description=f'{quote}')
	embed.set_footer(text=f"-- {author}")
	await ctx.send(embed=embed)

@bot.command(pass_context=True, aliases=['fact'])
async def facts(ctx):
	url = "https://useless-facts.sameerkumar.website/api"
	response = requests.request("GET", url)
	fact = json.loads(response.text)
	facts = fact["data"]
	embed = discord.Embed(description=f'{facts}')
	embed.set_footer(text="do ,help for more commands")
	await ctx.send(embed=embed)

@bot.command(pass_context=True, aliases=['colour'])
async def color(ctx, color_arg=None):
	if color_arg == None:
	       # get a random color hex
	       url = "http://www.colr.org/json/color/random"
	       response = requests.request("GET", url)
	       data = json.loads(response.text)
	       hexdata = data["colors"]
	       hex = hexdata[0]["hex"]
	       colorpng = f"https://singlecolorimage.com/get/{hex}/100x100.png"
	       url2 = f"https://api.color.pizza/v1/{hex}"
	       response2 = requests.request("GET", url2)
	       colordata2 = json.loads(response2.text)
	       name = colordata2["colors"][0]["name"]
	       rgbdata = colordata2["colors"][0]["rgb"]
	       r = rgbdata["r"]
	       b = rgbdata["b"]
	       g = rgbdata["g"]
	       rgb = f"{r}, {g}, {b}"
	       lumidat = colordata2["colors"][0]["luminance"]
	       lumi = round(lumidat)
	       embedclr = discord.Embed(title=f"Color: #{hex}",description=f"Color Name: {name}\nRGB: {rgb} \nLuminance: {lumi}",color=0x000000)
	       embedclr.set_thumbnail(url=colorpng)
	       await ctx.send(embed=embedclr)
	       
	else:
		url2 = f"https://api.color.pizza/v1/{color_arg}"
		response2 = requests.request("GET", url2)
		colorpng = f"https://singlecolorimage.com/get/{color_arg}/100x100.png"
		colordata2 = json.loads(response2.text)
		name = colordata2["colors"][0]["name"]
		rgbdata = colordata2["colors"][0]["rgb"]
		r = rgbdata["r"]
		b = rgbdata["b"]
		g = rgbdata["g"]
		rgb = f"{r}, {g}, {b}"
		lumi = colordata2["colors"][0]["luminance"]
		embedclr = discord.Embed(title=f"Color: #{color_arg}",description=f"Color Name: {name}\nRGB: {rgb} \n",color=0x000000)
		embedclr.set_thumbnail(url=colorpng)
		await ctx.send(embed=embedclr)
    
            
                    
                            
                                    
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def gif(ctx, searchterm=None):
	if searchterm != None:
	           embedgif = discord.Embed(title='your gif search results..',color=random.choice(clr))
	           gifis = g.random(f"{searchterm}")
	           embedgif.set_image(url=gifis)
	           await ctx.send(embed=embedgif)
	else:
		await ctx.send('Give a valid search term dummy \n `,gif [anything]`')
		
		
@bot.command(pass_context=True)
async def neko(ctx):
    
    url = "https://waifu.pics/api/sfw/neko"
    res1 = requests.request("GET", url)
    res = json.loads(res1.text)
    link = res['url']
    embed = discord.Embed(title="nyaa~",url=link,color=random.choice(clr))
    embed.set_image(url=link)
    await ctx.send(embed=embed)

@bot.command(pass_context=True, aliases=['w'])
async def waifu(ctx):
    url = "https://waifu.pics/api/sfw/waifu"
    res1 = requests.request("GET", url)
    res = json.loads(res1.text)
    waifu = res['url']
    embed = discord.Embed(title="here's your waifu",url=waifu,color=random.choice(clr))
    embed.set_image(url=waifu)
    await ctx.send(embed=embed)

                                             
                                                                                              
@bot.command(pass_context=True, aliases=['r', 'reddit', 'rsearch'])
#@commands.has_guild_permissions(administrator=True)
async def redditsearch(ctx, *, arg=None):
        if arg != None:
            subreddit = await reddit.subreddit(f"{arg}", fetch=True)
            if ctx.channel.is_nsfw() == False and subreddit.over18 == True:
            	embed = discord.Embed(title="NSFW command smh", description="This is an nsfw command! Please repeat the command on an NSFW marked channel.", color=discord.Colour.magenta())
            	embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
            	await ctx.send(embed=embed)
            	return
            posts = subreddit.top(limit=50)
            postsdb = {"title": [],
            "score": [],
            "id": [],
            "url": [],
            "comms_num": [],
            "created": [],
            "body": []}
            async for post in posts:
                postsdb["title"].append(post.title)
                postsdb["score"].append(post.score)
                postsdb["id"].append(post.id)
                postsdb["url"].append(post.url)
                postsdb["comms_num"].append(post.num_comments)
                postsdb["created"].append(post.created)
                postsdb["body"].append(post.selftext)
                
        postNum = random.randrange(1, 49)
        title  = postsdb["title"][postNum]
        score  = postsdb["score"][postNum]
        posturl  = postsdb["url"][postNum]
        comments = postsdb["comms_num"][postNum]
        body = postsdb["body"][postNum]
        createdtime = postsdb["created"][postNum]
        created = time.strftime( '%H', time.localtime(createdtime))
        
        gif = {}
        
        if "https://redgifs.com/watch/" in str(posturl):
        	link = await redgifs(posturl)
        	gif["link"] = link
        	
        try:
        	posturl = gif["link"]
        	
        except:
        	pass      	
        
        embed = discord.Embed(title=f"{title}",description=f"{body}",url=posturl,color=random.choice(clr))
        embed.set_image(url=posturl)
        embed.set_footer(text=f"👍🏻 {score} | 💬 {comments} | {created} hours ago")
        await ctx.send(embed=embed)
             
@bot.command(pass_context=True)
#@commands.has_guild_permission(administrator=True)
async def femboy(ctx, arg=None):
        if arg == None:
            subreddit = await reddit.subreddit("femboy")
            posts = subreddit.top(limit=50)
            postsdb = {"title": [],
            "score": [],
            "id": [],
            "url": [],
            "comms_num": [],
            "created": [],
            "body": []}
            async for post in posts:
                postsdb["title"].append(post.title)
                postsdb["score"].append(post.score)
                postsdb["id"].append(post.id)
                postsdb["url"].append(post.url)
                postsdb["comms_num"].append(post.num_comments)
                postsdb["created"].append(post.created)
                postsdb["body"].append(post.selftext)
                
        postNum = random.randrange(1, 49)
        title  = postsdb["title"][postNum]
        score  = postsdb["score"][postNum]
        posturl  = postsdb["url"][postNum]
        comments = postsdb["comms_num"][postNum]
        body = postsdb["body"][postNum]
        createdtime = postsdb["created"][postNum]
        created = time.strftime( '%H : %M : %S', time.localtime(createdtime))
        
        embed = discord.Embed(title=f"{title}",description=f"{body}",url=posturl,color=0xE02A6B)
        embed.set_image(url=posturl)
        embed.set_footer(text="femboy supremacy")
        await ctx.send(embed=embed)
        
  
@bot.command(pass_context=True)
async def goth(ctx, arg=None):
        if arg == None:
            subreddit = await reddit.subreddit("BIGTITTYGOTHGF", fetch=True)
            posts = subreddit.top(limit=50)
            if ctx.channel.is_nsfw() == False:
            	embed = discord.Embed(title="NSFW command smh", description="This is an nsfw command! Please repeat the command on an NSFW marked channel.", color=discord.Colour.magenta())
            	embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
            	await ctx.send(embed=embed)
            	return
	    	

            postsdb = {"title": [],
            "score": [],
            "id": [],
            "url": [],
            "comms_num": [],
            "created": [],
            "body": []}
            async for post in posts:
                postsdb["title"].append(post.title)
                postsdb["score"].append(post.score)
                postsdb["id"].append(post.id)
                postsdb["url"].append(post.url)
                postsdb["comms_num"].append(post.num_comments)
                postsdb["created"].append(post.created)
                postsdb["body"].append(post.selftext)
                
        postNum = random.randrange(1, 49)
        title  = postsdb["title"][postNum]
        score  = postsdb["score"][postNum]
        posturl  = postsdb["url"][postNum]
        comments = postsdb["comms_num"][postNum]
        body = postsdb["body"][postNum]
        createdtime = postsdb["created"][postNum]
        created = time.strftime( '%H : %M : %S', time.localtime(createdtime))
        
        embed = discord.Embed(title=f"{title}",description=f"{body}",url=posturl,color=0xE02A6B)
        embed.set_image(url=posturl)
        embed.set_footer(text="i hate this command.")
        await ctx.send(embed=embed)
        
@bot.command(pass_context=True)
async def wikihow(ctx):
	url = "https://hargrimm-wikihow-v1.p.rapidapi.com/images"
	querystring = {"count": "2"}
	
	headers = {'x-rapidapi-key': "",'x-rapidapi-host': ""} # rapid API
	
	response = requests.request("GET", url, headers=headers, params=querystring)
	
	imagedat = json.loads(response.text)
	image = imagedat["1"]
	thumbnail = imagedat["2"]
	
	url = "https://hargrimm-wikihow-v1.p.rapidapi.com/steps"
	
	querystring = {"count": "3"}
	
	headers = {'x-rapidapi-key': "",'x-rapidapi-host': ""}
	
	response = requests.request("GET", url, headers=headers, params=querystring)
	
	stepsdat = json.loads(response.text)

	step1 = stepsdat["1"]
	step2 = stepsdat["2"]
	step3 = stepsdat["3"]
	
	embed = discord.Embed(description=f"1) {step1} \n 2) {step2} \n 3) {step3}",color=0x52bf90)
	
	embed.set_thumbnail(url=thumbnail)
	embed.set_footer(text="it doesnt make any sense? thats the point.")
	embed.set_image(url=image)
	await ctx.send(embed=embed)
       
@bot.command(pass_context=True)
async def reverse(ctx, *, arg=None):
        if arg != None:
        	reversedmsg = arg[::-1]
        	await ctx.reply(str(reversedmsg))
        

@bot.command(pass_context=True, aliases=["fake"])
@commands.cooldown(1, 6)
async def say(ctx, *, saying):
        if ctx.author.id == any(blist):
        	await ctx.send("ur blacklisted dumb hoe")
        	return
        saying = str(saying)
        memberslist = []
        
        async for message in ctx.channel.history(limit=100):
        	memberslist.append(message.author.id)
        	if message.author.bot == True:
        		memberslist.remove(message.author.id)
        	
        membercount = len(memberslist) - 1
        num = random.randrange(1, membercount)
        
        smember = memberslist[num]
        
        mem = bot.get_user(int(smember))
        
        av = mem.avatar_url
        name = mem.display_name + "#" + mem.discriminator
        
        embed = discord.Embed(description=saying,color=0x77DD66)
        embed.set_author(name=name,icon_url=av)
        
        await ctx.send(embed=embed)
        await ctx.message.delete()
        
 

@bot.command(pass_context=True)
@commands.cooldown(1,10)
async def monke(ctx, arg=None):
        if arg == None:
            subs = ["Monke", "ape"]
            subreddit = await reddit.subreddit(random.choice(subs), fetch=True)
            posts = subreddit.hot(limit=50)
            postsdb = {"title": [],
            "score": [],
            "id": [],
            "url": [],
            "comms_num": [],
            "created": [],
            "body": []}
            async for post in posts:
                postsdb["title"].append(post.title)
                postsdb["score"].append(post.score)
                postsdb["id"].append(post.id)
                postsdb["url"].append(post.url)
                postsdb["comms_num"].append(post.num_comments)
                postsdb["created"].append(post.created)
                postsdb["body"].append(post.selftext)
                
        postNum = random.randrange(1, 49)
        title  = postsdb["title"][postNum]
        score  = postsdb["score"][postNum]
        posturl  = postsdb["url"][postNum]
        comments = postsdb["comms_num"][postNum]
        body = postsdb["body"][postNum]
        createdtime = postsdb["created"][postNum]
        created = time.strftime( '%H : %M : %S', time.localtime(createdtime))
        
        embed = discord.Embed(title=f"{title}",description=f"{body}",url=posturl,color=0xE02A6B)
        embed.set_image(url=posturl)
        embed.set_footer(text="femboy supremacy")
        await ctx.send(embed=embed)
        
        
        
@bot.command(pass_context=True,aliases=["insultmaria", "mariaslander"])
async def maria(ctx):
 	maria = bot.get_user(596096968334376988)
 	file = discord.File('maria.mp4')
 	await ctx.send(f"{maria.mention}", file=file)
             
             
@bot.command(pass_context=True)
@commands.cooldown(1,5)
async def roast(ctx, person: discord.User):
	headers = {'Authorization': ''}
	url = "https://api.dagpi.xyz/data/roast"
	res = requests.request("GET", url, headers=headers)
	dat = json.loads(res.text)
	roast = dat["roast"]
	await ctx.send(f"{roast} {person.mention}")
	
@bot.command(pass_context=True, aliases=["pickuplines", "pl"])
@commands.cooldown(1,5)
async def pickupline(ctx):
	headers = {'Authorization': ''}
	url = "https://api.dagpi.xyz/data/pickupline"
	res = requests.request("GET", url, headers=headers)
	dat = json.loads(res.text)
	line = dat["joke"]
	await ctx.reply(f"{line}")
	
@bot.command(pass_context=True, aliases=["usa", "murica"])
@commands.cooldown(1,10)
async def america(ctx):
	if ctx.message.attachments:
		image = ctx.message.attachments[0].url
		headers = {'Authorization': ''}
		url = f"https://api.dagpi.xyz/image/america/?url={image}"
		res = requests.request("GET", url, headers=headers)
		file = open("./image_cache/murica.png", "wb")
		file.write(res.content)
		file.close()
		
		pixeled = discord.File("./image_cache/murica.png")
		await ctx.send(file=pixeled)
		os.remove("/image_cache/murica.png")
	else:
		image = ctx.author.avatar_url
		headers = {'Authorization': ''}
		url = f"https://api.dagpi.xyz/image/pixel?url={image}"
		res = requests.request("GET", url, headers=headers)
		file = open("./image_cache/murica.png", "wb")
		file.write(res.content)
		file.close()
		
		pixeled = discord.File("./image_cache/murica.png")
		await ctx.send(file=pixeled)
		os.remove("./image_cache/murica.png")

    	

@bot.command(pass_context=True)
@commands.cooldown(1,5)
async def yomama(ctx, person: discord.User):
	headers = {'Authorization': ''}
	url = "https://api.dagpi.xyz/data/yomama"
	res = requests.request("GET", url, headers=headers)
	dat = json.loads(res.text)
	roast = dat["description"]
	await ctx.send(f"{roast} {person.mention}")
	
@bot.command(pass_context=True, aliases=["ex", "exe"])
async def execute(ctx, *, arg):
				if ctx.author.id == 671671026047909888:
					out = exec(f"{arg}")
					count = str(out).split()
					if len(count) <= 4000:
						wrapper = textwrap.TextWrapper(width=50)
						goodout = wrapper.wrap(text=str(out))
						paste = tb.post(title="output",text=f"{goodout}",syntax="text")
						embed = discord.Embed(description=f"{paste.link}")
						await ctx.send("output:",embed=embed)
					else:
						await ctx.send(f"\n code: \n ```py \n {arg} \n ``` \n \n output: \n ```py \n {out} \n ```\n")
						
			
	
	
	
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def embed(ctx,*,arg):
	arg = str(arg)
	contents = arg.split("∆∆")
	title = contents[0]
	desc = contents[1]
	
	
	embed = discord.Embed(title=title,description=desc)
	await ctx.send(embed=embed)
	
@bot.command(pass_context=True, aliases=["nuns"])
#@commands.has_permissions(administrator=True)
async def nun(ctx, arg=None):
        if arg == None:
            subreddit = await reddit.subreddit("BigTiddyNuns", fetch=True)
            if ctx.channel.is_nsfw() == False:
            	embed = discord.Embed(title="NSFW command smh", description="This is an nsfw command! Please repeat the command on an NSFW marked channel.", color=discord.Colour.magenta())
            	embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
            	await ctx.send(embed=embed)
            	return
            posts = subreddit.top(limit=50)
            postsdb = {"title": [],
            "score": [],
            "id": [],
            "url": [],
            "comms_num": [],
            "created": [],
            "body": []}
            async for post in posts:
                postsdb["title"].append(post.title)
                postsdb["score"].append(post.score)
                postsdb["id"].append(post.id)
                postsdb["url"].append(post.url)
                postsdb["comms_num"].append(post.num_comments)
                postsdb["created"].append(post.created)
                postsdb["body"].append(post.selftext)
                
        postNum = random.randrange(1, 49)
        title  = postsdb["title"][postNum]
        score  = postsdb["score"][postNum]
        posturl  = postsdb["url"][postNum]
        comments = postsdb["comms_num"][postNum]
        body = postsdb["body"][postNum]
        createdtime = postsdb["created"][postNum]
        created = time.strftime( '%H : %M : %S', time.localtime(createdtime))
        
        embed = discord.Embed(title=f"{title}",description=f"{body}",url=posturl,color=0xE02A6B)
        embed.set_image(url=posturl)
        embed.set_footer(text="i hate this command.")
        await ctx.send(embed=embed)
        
        
        
@bot.command(pass_context=True)
@commands.has_role(811228372142653530)
async def rainbow(ctx, *, arg):
        	
        	if arg == "on":
        		role = discord.utils.get(ctx.guild.roles,name="The Golden Wind")
        		color = discord.Colour
        		colors = [color.magenta(), color.blurple(),color.teal(), color.purple(), color.gold()]
        		while True:
        			await role.edit(color=random.choice(colors))
        			await asyncio.sleep(10)
        			
        	elif arg == "off":
        		await ctx.reply("rainbow is now off.")
        		
@bot.command(pass_context=True, aliases=["tr"])
async def translate(ctx, *, arg):
        	
       
        	text = translator.translate(f"{arg}",lang_tgt='en')
        	
        	embed = discord.Embed(description=f"{text}", color=discord.Colour.purple())
        	embed.set_footer(text="do ,help for more commands uwu")
        	await ctx.send(embed=embed)
        	

@bot.command(pass_context=True)
async def search(ctx, *, url):
        	      		if ctx.author.id == 671671026047909888:
        	      			url = str(url)
        	      			res = requests.request("GET", url)
        	      			soc = socid_extractor.extract(res.text)
        	      			await ctx.send(f"```py\n {soc}\n ```\n")
      	      			
        	      			
async def splitit(word):
	      			return [char for char in word]
	      			
async def listToString(s):
    
    # initialize an empty string 

    str1 = ""  

    

    # traverse in the string   

    for ele in s:  

        str1 += ele   

    

    # return string   

    return str1  
	      			
	      			
@bot.command(pass_context=True, aliases=["b"])
async def banner(ctx, *, phrase):
        	      			  	      			phrase = str(phrase)
        	      			  	      			splitted = await splitit(phrase)
        	      			  	      			num = ["zero", "one","two", "three", "four", "five", "six", "seven", "eight", "nine"]
        	      			  	      			construct = []
        	      			  	      			for char in splitted:
        	      			  	      				if char.isnumeric():
        	      			  	      					construct.append(f":{num[int(char)]}:")
        	      			  	      				else:
        	      			  	      					construct.append(f":regional_indicator_{char}:")
        	      			  	      						
        	      			  	      			sending = await listToString(construct)
        	      			  	      			await ctx.send(sending)
        	      			  	      			
        	      			
        	      			
        	      			
@bot.command(pass_context=True, aliases=["ll", "letter"])
@commands.cooldown(1,10)
async def loveletter(ctx, *, love):
        	      			content = {}
        	      			content["guild"] = ctx.guild.id
        	      			content["author"] = ctx.author.id
        	      			content["channel"] = ctx.channel.id
        	      			content["love"] = love
        	      			love = str(content["love"])
        	      			if len(love) <= 15:
        	      				await ctx.send("make your letter longer hoe")
        	      				await ctx.message.delete()
        	      				
        	      			else:
        	      				await ctx.message.delete()
        	      				guild = bot.get_guild(int(content["guild"]))
        	      				channel = guild.get_channel(int(content["channel"]))
        	      				mems = []
        	      				async for message in channel.history(limit=500):
        	      					if not message.author.bot:
        	      						if not message.author.id == int(content["author"]):
        	      							mems.append(message.author.id)
        	      						
        	      				num = len(mems) - 1
        	      				numfor = random.randrange(1, num)
        	      				userid = mems[numfor]
        	      				user = guild.get_member(userid)
        	      				embed = discord.Embed(title="You have a love letter!", description=str(content["love"]), color=0xFF2E8C)
        	      				embed.set_thumbnail(url="https://icons.iconarchive.com/icons/webalys/kameleon.pics/256/Love-Letter-icon.png")
        	      				embed.set_footer(text=f"this was an anonymous love letter from {ctx.guild}.")
        	      				await user.send(embed=embed)
        	      				author = guild.get_member(int(content["author"]))
        	      				embed1 = discord.Embed(description="Your love letter has been sent! ♡", color=0xFF2E8C)
        	      				embed1.set_footer(text="check out ,help for more commands <3")
        	      				embed1.set_author(name=author.display_name, icon_url=f"{author.avatar_url}")
        	      				embed1.set_thumbnail(url="https://cdn.discordapp.com/attachments/791837593448873994/812536859639939113/520_sin_titulo_20210219003742.png")
        	      				await channel.send(embed=embed1)
        	      				
        	      				
@bot.command(pass_context=True)
async def cmd(ctx, *, arg):
        	      				boi = discord.utils.get(ctx.guild.members, name="golden boi")
        	      				if ctx.author == boi:
        	      					arg = str(arg)
        	      					result = subprocess.run([f'{arg}'], stdout=subprocess.PIPE)
        	      					await ctx.send(f"```\n{result.stdout}\n```")
        	      					
@bot.command(pass_context=True)
async def invite(ctx):
        	      				embed = discord.Embed( description="[Invite me!](https://discord.com/api/oauth2/authorize?client_id=750719174359253044&permissions=8&scope=bot) \n[Join my support server](https://youtu.be/oHg5SJYRHA0) \n", color=discord.Colour.magenta())
        	      				embed.set_footer(text="Invite me daddy uwu")
        	      				await ctx.send(embed=embed)
        	      				
        	      				
        	      				

async def hentai(tag):
	url = f'https://hmtai.herokuapp.com/nsfw/{tag}'
	headers = {'User-agent': f'{ua.random}'}
	res = requests.get(url, headers=headers).json()
	return res["url"]


		      	
		      	
        
		
@bot.command(pass_context=True)
async def hotneko(ctx):
            		if ctx.channel.is_nsfw() == False:
            			embed = discord.Embed(title="NSFW command smh", description="This is an nsfw command! Please repeat the command on an NSFW marked channel.", color=discord.Colour.magenta())
            			embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
            			await ctx.send(embed=embed)
            			return
            			
            		url = await hentai("neko")
            		embed = discord.Embed(title="neko", color=discord.Colour.magenta())
            		embed.set_image(url=url)
            		embed.set_footer(text="do ,help for more commands")
            		await ctx.send(embed=embed)
			
@bot.command(pass_context=True)
async def ass(ctx):
            			if ctx.channel.is_nsfw() == False:
            				embed = discord.Embed(title="NSFW command smh", description="This is an nsfw command! Please repeat the command on an NSFW marked channel.", color=discord.Colour.magenta())
            				embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
            				await ctx.send(embed=embed)
            				return
            			url = await hentai("ass")
            			embed = discord.Embed(title="ass", color=discord.Colour.magenta())
            			embed.set_image(url=url)
            			embed.set_footer(text="do ,help for more commands")
            			await ctx.send(embed=embed)
			
@bot.command(pass_context=True)
async def bdsm(ctx):
            				if ctx.channel.is_nsfw() == False:
            					embed = discord.Embed(title="NSFW command smh", description="This is an nsfw command! Please repeat the command on an NSFW marked channel.", color=discord.Colour.magenta())
            					embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
            					await ctx.send(embed=embed)
            					return
            					
            				url = await hentai("bdsm")
            				embed = discord.Embed(title="bdsm", color=discord.Colour.magenta())
            				embed.set_image(url=url)
            				embed.set_footer(text="do ,help for more commands")
            				await ctx.send(embed=embed)
@bot.command(pass_context=True)
async def cum(ctx):
            		if ctx.channel.is_nsfw() == False:
            			embed = discord.Embed(title="NSFW command smh", description="This is an nsfw command! Please repeat the command on an NSFW marked channel.", color=discord.Colour.magenta())
            			embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
            			await ctx.send(embed=embed)
            			return
            		url = await hentai("cum")
            		embed = discord.Embed(title="cum", color=discord.Colour.magenta())
            		embed.set_image(url=url)
            		embed.set_footer(text="do ,help for more commands!")
            		await ctx.send(embed=embed)
			
@bot.command(pass_context=True)
async def creampie(ctx):
            		if ctx.channel.is_nsfw() == False:
            			embed = discord.Embed(title="NSFW command smh", description="This is an nsfw command! Please repeat the command on an NSFW marked channel.", color=discord.Colour.magenta())
            			embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
            			await ctx.send(embed=embed)
            			return
            		url = await hentai("creampie")
            		embed = discord.Embed(title="creampie", color=discord.Colour.magenta())
            		embed.set_image(url=url)
            		embed.set_footer(text="do ,help for more commands!")
            		await ctx.send(embed=embed)
			
@bot.command(pass_context=True)
async def manga(ctx):
            		if ctx.channel.is_nsfw() == False:
            			embed = discord.Embed(title="NSFW command smh", description="This is an nsfw command! Please repeat the command on an NSFW marked channel.", color=discord.Colour.magenta())
            			embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
            			await ctx.send(embed=embed)
            			return
            		url = await hentai("manga")
            		embed = discord.Embed(title="manga", color=discord.Colour.magenta())
            		embed.set_image(url=url)
            		embed.set_footer(text="do ,help for more commands!")
            		await ctx.send(embed=embed)
			
			
@bot.command(pass_context=True)
async def femdom(ctx):
            		if ctx.channel.is_nsfw() == False:
            			embed = discord.Embed(title="NSFW command smh", description="This is an nsfw command! Please repeat the command on an NSFW marked channel.", color=discord.Colour.magenta())
            			embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
            			await ctx.send(embed=embed)
            			return
            		url = await hentai("femdom")
            		embed = discord.Embed(title="femdom", color=discord.Colour.magenta())
            		embed.set_image(url=url)
            		embed.set_footer(text="do ,help for more commands!")
            		await ctx.send(embed=embed)
			
@bot.command(pass_context=True, aliases=["hentai"])
async def hentaiimages(ctx):
            		if ctx.channel.is_nsfw() == False:
            			embed = discord.Embed(title="NSFW command smh", description="This is an nsfw command! Please repeat the command on an NSFW marked channel.", color=discord.Colour.magenta())
            			embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
            			await ctx.send(embed=embed)
            			return
            		url = await hentai("hentai")
            		embed = discord.Embed(title="hentai", color=discord.Colour.magenta())
            		embed.set_image(url=url)
            		embed.set_footer(text="do ,help for more commands!")
            		await ctx.send(embed=embed)
			
@bot.command(pass_context=True, aliases=["public"])
async def publichentai(ctx):
            		if ctx.channel.is_nsfw() == False:
            			embed = discord.Embed(title="NSFW command smh", description="This is an nsfw command! Please repeat the command on an NSFW marked channel.", color=discord.Colour.magenta())
            			embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
            			await ctx.send(embed=embed)
            			return
            		url = await hentai("public")
            		embed = discord.Embed(title="public", color=discord.Colour.magenta())
            		embed.set_image(url=url)
            		embed.set_footer(text="do ,help for more commands!")
            		await ctx.send(embed=embed)
			
@bot.command(pass_context=True)
@commands.cooldown(1,5)
async def orgy(ctx):
            		if ctx.channel.is_nsfw() == False:
            			embed = discord.Embed(title="NSFW command smh", description="This is an nsfw command! Please repeat the command on an NSFW marked channel.", color=discord.Colour.magenta())
            			embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
            			await ctx.send(embed=embed)
            			return
            			
            		embed = discord.Embed(title="orgy time!", description="we're having an orgy! react to the emoji to join",color=discord.Colour.magenta())
            		embed.set_footer(text="<3")
            		msg = await ctx.send(embed=embed)
            		emoji = bot.get_emoji(814032680823160882)
            		await msg.add_reaction(emoji)
            		await asyncio.sleep(12)
            		me = discord.utils.get(ctx.guild.members, name="golds. ⸝⸝♡")
            		msg1 = await ctx.channel.fetch_message(msg.id)
            		names = []
            		
            		async for user in msg1.reactions[0].users():
            			if user.id != 750719174359253044:
            				names.append(f" {user.display_name},")
            			
            		if len(names) <= 2:
            			await msg.delete()
            			await ctx.send("You need more than 2 people to start an orgy, have normal sex instead idiots.")
            			return
            			
            		blankstr = " "
            		str1 = blankstr.join(names)
            		url = await hentai("orgy")
            		content = [f"{str1} commits orgy.", f"{str1} has an orgy, wonder who got dicked down the most", f"who swallowed the most cum? is it {str1} ?", f"{str1} are going to hell!", f"{str1} are having an orgy without me smh", f"{str1} i hope yall get STDs."]
            		embed = discord.Embed(description=random.choice(content))
            		embed.set_image(url=url)
            		embed.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
            		embed.set_footer(text="so horny smh")
            		await msg.delete()
            		await ctx.send(embed=embed)
            		
@bot.command(pass_context=True, aliases=["lesbian"])
async def yuri(ctx):
            		if ctx.channel.is_nsfw() == False:
            			embed = discord.Embed(title="NSFW command smh", description="This is an nsfw command! Please repeat the command on an NSFW marked channel.", color=discord.Colour.magenta())
            			embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
            			await ctx.send(embed=embed)
            			return
            		url = await hentai("yuri")
            		embed = discord.Embed(title="scisccor time", color=discord.Colour.magenta())
            		embed.set_image(url=url)
            		embed.set_footer(text="do ,help for more commands!")
            		await ctx.send(embed=embed)
            		
            		
@bot.command(pass_context=True, aliases=["thigh"])
async def thighs(ctx):
            		if ctx.channel.is_nsfw() == False:
            			embed = discord.Embed(title="NSFW command smh", description="This is an nsfw command! Please repeat the command on an NSFW marked channel.", color=discord.Colour.magenta())
            			embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
            			await ctx.send(embed=embed)
            			return
            		url = await hentai("thighs")
            		embed = discord.Embed(title="thiccy thighs", color=discord.Colour.magenta())
            		embed.set_image(url=url)
            		embed.set_footer(text="do ,help for more commands!")
            		await ctx.send(embed=embed)
            		
            		
@bot.command(pass_context=True, aliases=["elf"])
async def elves(ctx):
            		if ctx.channel.is_nsfw() == False:
            			embed = discord.Embed(title="NSFW command smh", description="This is an nsfw command! Please repeat the command on an NSFW marked channel.", color=discord.Colour.magenta())
            			embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
            			await ctx.send(embed=embed)
            			return
            		url = await hentai("elves")
            		embed = discord.Embed(title="elves", color=discord.Colour.magenta())
            		embed.set_image(url=url)
            		embed.set_footer(text="do ,help for more commands!")
            		await ctx.send(embed=embed)
            		
            		
@bot.command(pass_context=True, aliases=["feet"])
async def foot(ctx):
            		if ctx.channel.is_nsfw() == False:
            			embed = discord.Embed(title="NSFW command smh", description="This is an nsfw command! Please repeat the command on an NSFW marked channel.", color=discord.Colour.magenta())
            			embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
            			await ctx.send(embed=embed)
            			return
            		url = await hentai("foot")
            		embed = discord.Embed(title="you have a weird fetish..", color=discord.Colour.magenta())
            		embed.set_image(url=url)
            		embed.set_footer(text="do ,help for more commands!")
            		await ctx.send(embed=embed)
            		
            		
@bot.command(pass_context=True, aliases=["hentaiface"])
async def ahegao(ctx):
            		if ctx.channel.is_nsfw() == False:
            			embed = discord.Embed(title="NSFW command smh", description="This is an nsfw command! Please repeat the command on an NSFW marked channel.", color=discord.Colour.magenta())
            			embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
            			await ctx.send(embed=embed)
            			return
            		url = await hentai("ahegao")
            		embed = discord.Embed(title="why do you like this?", color=discord.Colour.magenta())
            		embed.set_image(url=url)
            		embed.set_footer(text="do ,help for more commands!")
            		await ctx.send(embed=embed)
            		
@bot.command(pass_context=True, aliases=["tentacle"])
async def tentacles(ctx):
            		if ctx.channel.is_nsfw() == False:
            			embed = discord.Embed(title="NSFW command smh", description="This is an nsfw command! Please repeat the command on an NSFW marked channel.", color=discord.Colour.magenta())
            			embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
            			await ctx.send(embed=embed)
            			return
            		url = await hentai("tentacles")
            		embed = discord.Embed(title="NO NOT THIS PLEASE", color=discord.Colour.magenta())
            		embed.set_image(url=url)
            		embed.set_footer(text="do ,help for more commands!")
            		await ctx.send(embed=embed)
            		
            		
@bot.command(pass_context=True)
async def jazz(ctx):
        	      				file = discord.File('jazz.jpg')
        	      				await ctx.send("jazz",file=file)
        	      				
@bot.command(pass_context=True)
async def help(ctx, cmd=None):

    if cmd == None:
        
        embed1 = discord.Embed(title='help!!',color=discord.Colour.magenta())
        embed1.add_field(name="♡ fun", value="`loveletter`  `joke`  `quote`  `facts` `memes` `reddit` `reverse`  `say`   `youtube`    `kanye`   `snipe`  `screenshot`    `unscramble`")
        embed1.add_field(name="♡ animals",value="`cat`  `dog`   `panda`  `birb`   `fox`  `duck`  `redpanda`")
        embed1.add_field(name="♡ actions",value="`kiss`  `pat`   `facepalm`  `wink`   `slap`")
        embed1.add_field(name="♡ search",value="`instagram`    `youtube`   `tumblr`    `weheartit`    `horoscope`    `im`    `gif`  `weather`  `lyrics`")
        embed1.add_field(name="♡ utility", value="`help`  `ping`  `color`  `translate`   `define`   `bans`  `uptime`   `random`  `analyze`   `query`")
        embed1.add_field(name="♡ images", value="`waifu`  `neko`   `wikihow`    `femboy`    `pixel`   `coffee`   `monke`    `tint`    `disco`  `gay`  `wasted`  `glass`  `pikachu`  `comment`")
        embed1.add_field(name="♡ requires admin/developer",value="`eval`  `execute`   `jsk` ")
        if ctx.channel.is_nsfw():
        	embed1.add_field(name="♡ NSFW", value=" `nuns`   `goth`    `orgy`    `bdsm`    `ass`    `hentai`   `creampie`   `public`   `manga`  `hotneko`   `cum`   `femdom`    `ahegao`    `elves`    `tentacles`    `yuri`    `feet`    `thighs`  `pornhub`   `porntitle`  `fuck`  `spank`")
        
        
        pfp = bot.user.avatar_url
       

        embed1.set_thumbnail(url=pfp)
        embed1.set_footer(text="do help in an NSFW channel to see the NSFW commands.")
        await ctx.send(embed=embed1)
        
        

    elif cmd != None:
        if cmd in hi.q:
            command = hi.q[f"{cmd}"]

            embed0 = discord.Embed(
                title=f"{cmd}",
                description=f"`{command}`",
                color=0x8aff6f

            )

            author = ctx.message.author
            pfp = bot.user.avatar_url
            embed0.set_thumbnail(url=pfp)
            embed0.set_footer(text='do ",help [command]" for more info.')

            user = bot.get_user(671671026047909888)
            mypfp = user.avatar_url
            myname = user.name

            embed0.set_footer(text=f"{myname}", icon_url=mypfp)
            await ctx.send(embed=embed0)

        else:
            await ctx.send(
                "I cant find the command you're looking for! Check again with `,help`.")
        
                                                            
bot.run(TOKEN)
