#json
import urllib.request, json

import datetime,asyncio,os

# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord

# IMPORT THE OS MODULE.
import os

# IMPORT LOAD_DOTENV FUNCTION FROM DOTENV MODULE.
from dotenv import load_dotenv

# IMPORT COMMANDS FROM THE DISCORD.EXT MODULE.
from discord.ext import commands, tasks

# LOADS THE .ENV FILE THAT RESIDES ON THE SAME LEVEL AS THE SCRIPT.
load_dotenv()

# GRAB THE API TOKEN FROM THE .ENV FILE.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# CREATES A NEW BOT OBJECT WITH A SPECIFIED PREFIX. IT CAN BE WHATEVER YOU WANT IT TO BE.
bot = commands.Bot(command_prefix="$")


@bot.command()
async def ping(ctx):
	await ctx.channel.send("pong")

@bot.command(name="print")
async def print(ctx, arg):
	await ctx.channel.send(arg)

#{'success': True, 'stats': {'client_id': '0x4d5927d4d7c322330e4042b85b2a257cd6dc03df', 'win_total': 0, 'draw_total': 0, 'lose_total': 0, 'elo': 1200, 'rank': 2147483647, 'name': 'Code Support :heart:'}, 'cache': {'status': True, 'message': 'Daddy chill~', 'till_expiry': '3 hours, 57 minutes & 28 seconds'}}
@bot.command(name="astats")
async def axie(ctx, arg):

	url = urllib.request.urlopen("https://server.axie.watch/scholar?address="+ arg +"&pvp=true&slp=true")
	data = json.loads(url.read().decode())

	pve = urllib.request.urlopen("https://server.axie.watch/pve?address="+ arg +"")
	pdata = json.loads(pve.read().decode())

	if data['scholar']['blockchain_related']['signature'] is None:
		embedVar = discord.Embed(title="No Result", description="", color=0x00ff00)
		embedVar.add_field(name="Ronin Address", value=arg, inline=False)
		await ctx.channel.send(embed=embedVar)
	else:
		#info = data['cache']['till_expiry']
		#await ctx.channel.send(info)
		todaySLP = data['slp']['today']['slpAmount']
		yesterdaySLP = data['slp']['yesterday']['slpAmount']
		realToday = todaySLP-yesterdaySLP
		axieStats = discord.Embed(title="Freedom Fighter Helper", description="", color=0x00ff00)
		axieStats.add_field(name="Ronin Address", value=data['scholar']['client_id'], inline=False)
		axieStats.add_field(name="Scholar Name", value=data['pvp']['name'], inline=True)
		axieStats.add_field(name=":crossed_swords: MMR", value=data['pvp']['elo'], inline=True)
		axieStats.add_field(name=":trophy: Rank", value=data['pvp']['rank'], inline=True)
		axieStats.add_field(name=":dagger: Total Win(s)", value=data['pvp']['win_total'], inline=True)
		axieStats.add_field(name=":skull: Total Lose(s)", value=data['pvp']['lose_total'], inline=True)
		axieStats.add_field(name=":shield: Total Draw(s)", value=data['pvp']['draw_total'], inline=True)
		axieStats.add_field(name="Today SLP", value=realToday, inline=True)
		axieStats.add_field(name="Adventure SLP", value=''+ str(pdata['gained_slp_response']['gained_slp']) + ' / '+ str(pdata['gained_slp_response']['max_slp']) + '', inline=True)
		#axieStats.add_field(name="Adventure Today", value="", inline=True)
		#axieSLP.add_field(name=":slp:", value=""+ pdata['gained_slp_response']['gained_slp'] +"/"+ pdata['gained_slp_response']['max_slp'] +"", inline=True)
		await ctx.channel.send(embed=axieStats)


@bot.command(name="slp")
async def getslp(ctx):
		now = datetime.datetime.now()
		url = urllib.request.urlopen("https://api.coingecko.com/api/v3/simple/price?ids=smooth-love-potion,axie-infinity&vs_currencies=php")
		data = json.loads(url.read().decode())
		slpPrice = discord.Embed(title="CoinGecko | AXS/SLP", description="", color=0x00ff00)
		slpPrice.add_field(name="SLP", value="₱" + str(data['smooth-love-potion']['php']) +"", inline=True)
		slpPrice.add_field(name="AXS", value="₱" + str(data['axie-infinity']['php']) +"", inline=True)
		slpPrice.add_field(name="Date", value=now.strftime("%B %d, %Y %I:%M %p"), inline=False)
		await ctx.channel.send(embed=slpPrice)

@bot.event
async  def on_ready():
    	get_slp.start()
@tasks.loop(seconds=600)
async def get_slp():
		channel = bot.get_channel(884781333954576384)
		now = datetime.datetime.now()
		url = urllib.request.urlopen("https://api.coingecko.com/api/v3/simple/price?ids=smooth-love-potion,axie-infinity&vs_currencies=php")
		data = json.loads(url.read().decode())
		slpPrice = discord.Embed(title="CoinGecko | AXS/SLP", description="", color=0x00ff00)
		slpPrice.add_field(name="SLP", value="₱" + str(data['smooth-love-potion']['php']) +"", inline=True)
		slpPrice.add_field(name="AXS", value="₱" + str(data['axie-infinity']['php']) +"", inline=True)
		slpPrice.add_field(name="Date", value=now.strftime("%B %d, %Y %I:%M %p"), inline=False)
		await channel.send(embed=slpPrice)
# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(DISCORD_TOKEN)