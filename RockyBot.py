import asyncio
import json
import math
import os
import random
import re
import time
import pickle

import asyncpraw
import discord
import matplotlib.pyplot as plt
import numpy as np
import requests
import uwuify
import wikipedia
from discord import channel, message, player
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext
from randfacts import get_fact
from scipy.interpolate import make_interp_spline

from features import Feature as features


bot = commands.Bot(command_prefix='$')

client = discord.Client()

def txt_increment(text_file):
    
    file = open(text_file,"r+")
    num = file.readline()
    num = int(num.strip())
    file.truncate(0)
    file.close()
    file = open(text_file,"r+")
    file.write(str((num + 1)))

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="sussus amogus?"))
    print('We have logged in as {0.user}'.format(client))

async def heartbeat():

    global ping_arr
    global time_ping
    ping_arr = np.array([])

    await client.wait_until_ready()
    while not client.is_closed():

        if len(ping_arr) < 16:

            ping_arr = np.append(ping_arr, int(round(client.latency * 1000,3)))
            time_ping = time.time()

        else:

            ping_arr = np.delete(ping_arr, 0)
            ping_arr = np.append(ping_arr, int(round(client.latency * 1000,3)))
            time_ping = time.time()

        await asyncio.sleep(40)

general = client.get_channel(id=745066591443746857) # replace with channel_id
bot_commands = general = client.get_channel(id=745651510242836510)

@client.event
async def on_message(message):
    global channel_say

    msg = message.content
    
    if message.author == client.user:   
        return

    # if message.author.id == 866487511840063548 or message.author.id == 866713551295741962: 

    #     rng = random.randint(0,9)

    #     if rng == 0:
    #         await message.channel.send('**I am the better bot >:(**')
    if msg.startswith('$') and len(msg) >= 2:
        await features.txt_increment("stats.txt")
        with open('auth.pckl', 'rb+') as file:
            auth = pickle.load(file)
        if message.author not in auth:
            message.channel.send('You are not authorized. Run $help to authorize.')
        else:
            pass

    if msg.startswith('$hello'):
        await features.hello(message)

    if msg.startswith('$idsay'):
        await features.idsay(message)

    if msg.startswith('$say'):
        await features.say(message)
    
    if msg.startswith('$test'):
        await features.test(message)
        
    if msg.startswith('$art'):
        await features.art(message)

    if msg.startswith('$cat'):
        await features.cat(message)

    if msg.startswith('$196') or msg.startswith('$shitpost'):
        await features.sp(message)

    if msg.startswith('$truth'):
        await features.truth(message)

    if msg.startswith('$calc'):
        await features.calc(message)

    if msg.startswith('$ping'):
        await features.ping(message)

    if msg.startswith('$netgraph'):
        await features.netgraph(message)
    
    if msg.startswith('$graph'):
        await features.graphing(message)

    if msg.startswith('$info'):
        await features.info(message)

    if msg.startswith('$pfp'):
        await features.pfp(message)

    if msg.startswith('$github'):
        await features.github(message)

    if msg.startswith('$invite'):
        await features.invite(message)

    if msg.startswith('$flip'):
        await features.flip()

    if msg.startswith('$8ball'):
        await features.ball()

    if msg.startswith('$rps'):
        await features.rps(message)

    if (msg.startswith('gm') or msg.startswith('GM') or msg.startswith('good morning') or msg.startswith('Good morning')) and (msg != 'gmas') and (msg != 'GMAS'):
        await features.gm(message)

    if msg.startswith('gn') or msg.startswith('GN') or msg.startswith('good night') or msg.startswith('Good night'):
        await features.gn(message)

    if msg.startswith('gg') or msg.startswith('GG'):
        await features.gg(message)

    # if any(word in msg for word in ['69','420']):
    #     await message.channel.send('nice')

    # if any(word in msg for word in ['owo','OWO','uwu','UWU','oWo','uWu','UwU','OwO']) and message.author.id != 545025575295909899 and not msg.startswith('$uwuify'):
    #     # time_uwu = time.time()
    #     await message.channel.send('uwu')

    if any(word in msg for word in ['mai san','maisan','MAI SAN','MAISAN','mai-san','Mai-san','MAI-SAN']):
        await features.mai()

    if msg.startswith('$status'):
        await features.stats()
    
    if msg.startswith('$hmm'):
        await features.hmm()

    if msg.startswith('$kill'):
        await features.kill()

    if msg.startswith('$help'):
        await features.help()
    
    if msg.startswith('$secret'):
        await features.secret()
    
    if msg.startswith('$copycat'):
        await features.copycat()
    
    if msg.startswith('$uwuify'):
        await features.uwu()
    
    if msg.startswith('$stats'):
        await features.stats()

    if msg.startswith('$hug'):
        await features.hug()

    if msg.startswith('$setwikilang'):
        await features.setlang()

    if msg.startswith('$wiki'):
        await features.wiki()

    if msg.startswith('$randomwikipage'):
        await features.randomwiki()

    if msg.startswith('$fact'):
        await features.fact()

    # if msg.startswith('$spotify'):
    #     print('made it here')
    #     txt_increment("stats.txt")
    #     user = message.author
    #     print('made it here')
    #     for activity in user.activities:
    #         if isinstance(activity, discord.Spotify):
    #             print('made it here')
    #             await message.channel.send(f"{user} is listening to {activity.title} by {activity.artist}")
    #             print('made it here')

    if msg == '$blackjackinfo':
        await features.blackjackinfo()

    if msg == '$blackjackstats':
        await features.blackjackstats()

    if msg == '$blackjack': 
        await features.blackjack()

# bot ideas:
# yell at people if 3 people in a row say 'I' or '.'

# blackjack:
# 2 face up to player
# 1 face up 1 face down to bot
# ace can be both 1 or 11
# face cards are 10
# <= 16 bot takes >= 17 bot stands


# @bot.command()
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

client.loop.create_task(heartbeat())
client.run(os.getenv('discordtoken'))

# client.get_channel(745066591443746857).send('*System Restart*')
# client.get_channel(745066591443746857).send('*Bot Online*')
