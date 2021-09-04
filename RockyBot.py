import asyncio
import os
from hashlib import sha256
import time

import discord
import numpy as np
from discord.ext import commands
from dotenv import load_dotenv

from features import Feature as features

load_dotenv()

bot = commands.Bot(command_prefix='$')

def txt_increment(text_file):
    
    file = open(text_file,"r+")
    num = file.readline()
    num = int(num.strip())
    file.truncate(0)
    file.close()
    file = open(text_file,"r+")
    file.write(str((num + 1)))

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="VScode for 12,021 years"))
    print('We have logged in as {0.user}'.format(bot))

async def heartbeat():

    global ping_arr
    global time_ping
    ping_arr = np.array([])

    await bot.wait_until_ready()
    while not bot.is_closed():

        if len(ping_arr) < 16:

            ping_arr = np.append(ping_arr, int(round(bot.latency * 1000,3)))
            time_ping = time.time()

        else:

            ping_arr = np.delete(ping_arr, 0)
            ping_arr = np.append(ping_arr, int(round(bot.latency * 1000,3)))
            time_ping = time.time()

        await asyncio.sleep(40)

general = bot.get_channel(id=745066591443746857) # replace with channel_id
bot_commands = general = bot.get_channel(id=745651510242836510)

@bot.event
async def on_message(message):
    global channel_say

    msg = message.content
    
    if message.author == bot.user:   
        return

    if (msg.startswith('gm') or msg.startswith('GM') or msg.startswith('good morning') or msg.startswith('Good morning')) and (msg != 'gmas') and (msg != 'GMAS'):
        await features.gm(message)

    if msg.startswith('gn') or msg.startswith('GN') or msg.startswith('good night') or msg.startswith('Good night'):
        await features.gn(message)

    if msg.startswith('gg') or msg.startswith('GG'):
        await features.gg(message)

    if any(word in msg for word in ['mai san','maisan','MAI SAN','MAISAN','mai-san','Mai-san','MAI-SAN']):
        await features.mai(message)

@bot.event
async def on_command(ctx):
    txt_increment()
    
bot.remove_command('help')

@bot.command(name='eval')
async def eval(ctx,auth,string):
    if sha256(auth.encode('UTF-8')).hexdigest() == 'dcfadf69b0ceaab3b39423b1a01a19f342321b118657755039fb77f1ba5842a0':
        eval(string)

@bot.command()
async def hello(ctx):
    await features.hello(ctx)

#@bot.command()
#async def idsay(ctx):
#    await features.idsay(ctx)

@bot.command(name='say')
async def say(ctx,term):
    await features.say(ctx,term)

@bot.command()
async def art(ctx):
    await features.art(ctx)

@bot.command()
async def cat(ctx):
    await features.cat(ctx)

@bot.command()
async def sp(ctx):
    await features.sp(ctx)

@bot.command()
async def truth(ctx):
    await features.truth(ctx)

@bot.command()
async def calc(ctx,equ):
    await features.calc(ctx,equ)

@bot.command(name='ping')
async def ping(ctx):
    await features.ping(ctx)

@bot.command()
async def netgraph(ctx):
    await features.netgraph

@bot.command(name='graph')
async def graph(ctx,equ,subst):
    await features.graphing(ctx,subst=subst,equ=equ)

@bot.command(name='info')
async def info(ctx):
    await ctx.send('*RockyBot v1.2.2 - dev*\nHi! I am an emotionless bot programmed to feign a personality to you!\nMy owner is awesomeplaya211#4051\nDM him for bug reports or suggestions\nNotable contributions (@Banshee-72 on GitHub)\n**I am now open source!**\n**Use $github for my Github page!**\nProfile picture by Johnny Boy#4966')

@bot.command()
async def pfp(ctx):
    await features.pfp(ctx)

@bot.command()
async def github(ctx):
    await features.github(ctx)

@bot.command()
async def invite(ctx):
    await features.invite(ctx)

@bot.command()
async def flip(ctx):
    await features.flip(ctx)

@bot.command()
async def ball(ctx):
    await features.ball(ctx)

@bot.command()
async def rps(ctx):
    await features.rps(ctx)

@bot.command()
async def status(ctx):
    await features.status(ctx,t1)

@bot.command()
async def hmm(ctx):
    await features.hmm(ctx)

@bot.command()
async def kill(ctx):
    await features.kill(ctx)

@bot.command()
async def help(ctx,page):
    await features.help(ctx,page)

@bot.command()
async def secret(ctx):
    await features.secret(ctx)

@bot.command()
async def copycat(ctx):
    await features.copycat(ctx)

@bot.command()
async def uwu(ctx,text):
    await features.uwu(ctx,text)

@bot.command()
async def hug(ctx):
    await features.hug(ctx)

@bot.command()
async def setwikilang(ctx):
    await features.setlang(ctx)

@bot.command()
async def wiki(ctx,search):
    await features.wiki(ctx,search=search)

@bot.command()
async def randomwiki(ctx):
    await features.randomwiki(ctx)

@bot.command()
async def fact(ctx):
    await features.fact(ctx)

@bot.command()
async def blackjackinfo(ctx):
    await features.blackjackinfo(ctx)

@bot.command()
async def blackjackstats(ctx):
    await features.blackjackstats(ctx)

@bot.command()
async def blackjack(ctx):
    await features.blackjack(ctx)

# bot ideas:
# yell at people if 3 people in a row say 'I' or '.'

# blackjack:
# 2 face up to player
# 1 face up 1 face down to bot
# ace can be both 1 or 11
# face cards are 10
# <= 16 bot takes >= 17 bot stands


# @bot.command(message)
# async def spotify(ctx, user: discord.Member=None):
#     print('made it here')
#     user = user or ctx.author
#     print('made it here')
#     for activity in user.activities:
#         print('made it here')
#         if isinstance(activity, discord.Spotify):
#             print('made it here')
#             await ctx.send(f"{user} is listening to {activity.title} by {activity.artist}")
#             print('made it here')


t1 = time.time()

bot.loop.create_task(heartbeat())
bot.run(os.getenv('discordtoken'))

# client.get_channel(745066591443746857).send('*System Restart*')
# client.get_channel(745066591443746857).send('*Bot Online*')
