import asyncio
import json
import math
import os
import random
import re
import time

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
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix='$')

client = discord.Client()
global time_uwu
time_uwu = time.time()

reddit = asyncpraw.Reddit(
    client_id="MZgXIeYJm5rsrFHm9uWCeA",
    client_secret=os.getenv('reddittoken'),
    user_agent="discord:GenericBot:v1.2.2 (by /u/awesomeplaya211)"
)


def txt_increment(text_file):

    file = open(text_file,"r+")
    num = file.readline()
    num = int(num.strip())
    file.truncate(0)
    file.close()
    file = open(text_file,"r+")
    file.write(str((num + 1)))

def blackjack_increment(text_file, index):


    file = open(text_file,"r+")
    num = file.readline()
    num = num.strip().split()
    file.truncate(0)
    file.close()
    file = open(text_file,"r+")
    for i in range(len(num)):


        if i != index:
            file.write(str((int(num[i]))).rstrip('\n') + ' ')
            
        else:
            file.write(str((int(num[i]) + 1)).rstrip('\n') + ' ')





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

class Feature:

    global channel_say
    channel_say = 0

    async def hello(message):
        await message.channel.send('Hello!')
        txt_increment("stats.txt")

    async def idsay(message):
        txt_increment("stats.txt")
        if message.author.id == 538921994645798915:

            channel_say = client.get_channel(int(message.content[7:]))
            print('channel_say set to '+ message.content[7:])

    async def say(message):

        txt_increment("stats.txt")
        if message.author.id == 538921994645798915:

            await channel_say.send(message.content[5:])

    async def flag(message):
        txt_increment("stats.txt")
    
    async def test(message):
        await message.channel.send(message.author)
        txt_increment("stats.txt")

    async def art(message):
        txt_increment("stats.txt")
        subreddit = await reddit.subreddit("art")

        post_list = []

        count = 0
        async for submission in subreddit.top("week"):
            if count == 100:
                break
            if submission.over_18 == False and submission.is_self == False:
                # post_url = 'https://www.reddit.com'+submission.permalink
                post_list.append(submission)
                count += 1

        reddit_post = random.choice(post_list)
        await message.channel.send(reddit_post.title)
        await message.channel.send(reddit_post.url)
        await message.channel.send('Posted by u/'+reddit_post.author.name)
        await message.channel.send(str(reddit_post.score)+' upvotes')

    async def cat(message):
        txt_increment("stats.txt")
        subreddit = await reddit.subreddit("cats")

        post_list = []

        count = 0
        async for submission in subreddit.top("week"):
            if count == 100:
                break
            if submission.over_18 == False and submission.is_self == False and submission.link_flair_text == "Cat Picture":
                # post_url = 'https://www.reddit.com'+submission.permalink
                post_list.append(submission)
                count += 1

        reddit_post = random.choice(post_list)
        await message.channel.send(reddit_post.title)
        await message.channel.send(reddit_post.url)
        await message.channel.send('Posted by u/'+reddit_post.author.name)
        await message.channel.send(str(reddit_post.score)+' upvotes')



        async def sp():
        # https://cdn.discordapp.com/attachments/745066591443746857/879558411895848960/anime-couples.png
            txt_increment("stats.txt")
            with open("posts.txt") as file:

                lines = file.readlines()
                await message.channel.send(random.choice(lines))

        async def truth():
            txt_increment("stats.txt")
            with open("truth.txt") as file:

                lines = file.readlines()
                await message.channel.send(random.choice(lines))

    async def truth(message):
        txt_increment("stats.txt")
        with open("truth.txt") as file:

            lines = file.readlines()
            await message.channel.send(random.choice(lines))

    async def calc(message):


        txt_increment("stats.txt")
        await message.channel.send(str(eval(message.content[6:])))
       
    async def ping(message):
        await message.channel.send(f'Pong! Latency: {round(client.latency * 1000, 3)}ms')
        txt_increment("stats.txt")
    
    async def netgraph(message):
        txt_increment("stats.txt")

        time_since_ping = round(time.time() - time_ping)

        x = np.append(np.arange((len(ping_arr) - 1)*-40 , 1, 40) - time_since_ping, 0)
        y = np.append(ping_arr, ping_arr[len(ping_arr) - 1])

        X_ = np.linspace(min(x), max(x), 500)
        X_Y_Spline = make_interp_spline(x, y)
        Y_ = X_Y_Spline(X_)

        plt.plot(X_,Y_, color = 'red')

        plt.xlim(-600, 0)

        plt.ylim(0, max(Y_)*1.1)

        plt.xlabel('Time')

        plt.ylabel('Milliseconds')

        plt.title('Latency within the last 10 minutes')

        plt.savefig("test.png")




        file = discord.File("test.png") # an image in the same folder as the main bot file
        embed = discord.Embed() # any kwargs you want here
        embed.set_image(url="attachment://test.png")
        # filename and extension have to match (ex. "thisname.jpg" has to be "attachment://thisname.jpg")
        await message.channel.send(embed=embed, file=file)
        plt.clf()