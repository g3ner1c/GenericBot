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
import vexpy as vp
import wikipedia
from discord.ext import commands, tasks
from discord.utils import escape_markdown
from discord_slash import SlashCommand
from dotenv import load_dotenv
from pretty_help import PrettyHelp
from pyowm.owm import OWM
from randfacts import get_fact
from scipy.interpolate import make_interp_spline

from keep_alive import keep_alive

load_dotenv()

bot = commands.Bot(intents=discord.Intents.default(), command_prefix='$')

bot.help_command = PrettyHelp(color=0xae4dff) # 0xae4dff should be used for all embeds

global channel_say
channel_say = 0

# client = discord.Client()
slash = SlashCommand(bot, sync_commands=True)


global time_uwu
time_uwu = time.time()

reddit = asyncpraw.Reddit(
    client_id="MZgXIeYJm5rsrFHm9uWCeA",
    client_secret=os.getenv('reddittoken'),
    user_agent="discord:GenericBot:v1.4.0 (by /u/awesomeplaya211)"
)


async def heartbeat():

    global ping_arr
    global time_ping
    ping_arr = np.array([])

    await bot.wait_until_ready()
    while not bot.is_closed():

        if len(ping_arr) < 16:

            ping_arr = np.append(ping_arr, int(round(bot.latency * 1000, 3)))
            time_ping = time.time()

        else:

            ping_arr = np.delete(ping_arr, 0)
            ping_arr = np.append(ping_arr, int(round(bot.latency * 1000, 3)))
            time_ping = time.time()

        await asyncio.sleep(40)


# Setting `Playing ` status
# await bot.change_presence(activity=discord.Game(name="a game"))

# Setting `Streaming ` status
# await bot.change_presence(activity=discord.Streaming(name="My Stream", url=my_twitch_url))

# Setting `Listening ` status
# await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))

# Setting `Watching ` status
# await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))

playingStatus = ['Visual Studio Code', 'x86 Assembly', 'Titanfall 2', 'Team Fortress 2',
                 'SCP Containment Breach', 'osu!', 'Node.js', 'Minecraft', 'Hypixel Skywars', 'Genshin Impact', 'Factorio'
                 ]

watchingStatus = ['xQcOW', 'Wikipedia', 'The Bee Movie', 'Everyone',
                  'Mai-San'
                  ]

listeningStatus = ['to your VCs'
                   ]


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot), ' - ', bot.user.id)

    while True:

        statusType = random.randint(
            1, len(playingStatus)+len(watchingStatus)+len(listeningStatus))

        if statusType <= len(playingStatus):
            statusNum = random.randint(0, len(playingStatus) - 1)
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=playingStatus[statusNum]))

        elif statusType <= len(playingStatus)+len(watchingStatus):
            statusNum = random.randint(0, len(watchingStatus) - 1)
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=watchingStatus[statusNum]))

        elif statusType <= len(playingStatus)+len(watchingStatus)+len(listeningStatus):
            statusNum = random.randint(0, len(listeningStatus) - 1)
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=listeningStatus[statusNum]))

        await asyncio.sleep(10)


_8ball = ["Certainly yes", "Definentely Yes", "99.9% chance", "The chances are high", "Most likely",

          "Probably", "23% chance", "Not likely", "Don't count on it", "No way OMEGALUL",

          "Try it out and see!", "Ask again later", "Better not tell you now",

          "Cannot predict now", "Concentrate and ask again", "¯\_(ツ)_/¯"
          ]


@bot.command(brief='Completes text using AI',description='Completes the input text using the GPT-3 language model from OpenAI to imitate human text')
async def ai(ctx, *, input):
    response = requests.post(os.getenv('aiurl'), data='{"context":"' + input + '","topP":0.9,"temp":0.8,"response_length":128,"remove_input":true}').text
    generation = json.loads(response)[0]['generated_text']
    await ctx.send(generation)


@bot.command(brief='MIT license',description='Returns the MIT license to myself')
async def license(ctx):
    license = 'Copyright © 2021 awesomeplaya211 & Banshee-72 \n Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: \n The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. \nTHE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'
    await ctx.send('By using the bot you agree to the following license:')
    await ctx.send(license)


# @bot.command()
# # buggy lol
# async def graphing(ctx, subst, equ):
#     mequ = equ
#     x = np.linspace(-125, 125, 2501)
#     y = []
#     for i in range(len(x)):
#         value = x[i]
#         equ = re.sub('x', str(value), equ)
#         equ = equ[2:]
#         print(equ)
#         try:
#             res = eval(equ)
#         except:
#             res = 'Something Failed'
#         y.append(res)
#         equ = mequ
#     plt.xlim(-125, 125)
#     plt.ylim(-25, max(y)*1.1)
#     plt.plot(x, y)
#     plt.savefig("temp/graph.png")

#     file = discord.File("temp/graph.png")
#     embed = discord.Embed()
#     embed.set_image(url="attachment://graph.png")
#     await ctx.send(embed=embed, file=file)
#     plt.clf()


@bot.command(brief='Mute command',description='Mutes user. Administrator privileges required')
async def mute(ctx, member: discord.Member):

    if  ctx.author.id == 538921994645798915:

        guild = ctx.guild
        role = discord.utils.get(guild.roles, name='Muted')

        await member.add_roles(role)

        embed=discord.Embed(title="Bad user >:(", description="{0} has been muted".format(member), color=0xae4dff)
        
        await ctx.send(embed=embed)

    else:

        embed=discord.Embed(title="403 Forbidden :(", description="You don't have administrator privileges", color=0xae4dff)

        await ctx.send(embed=embed)


@bot.command(brief='Kick command',description='Kicks user out of the server. Administrator privileges required')
async def kick(ctx, member: discord.Member):

    if ctx.author.id == 538921994645798915:

        await member.kick()

        embed = discord.Embed(title = "{0} has been kicked".format(member), description = "Hope you didn't do that by accident lol", color = 0xae4dff)
        
        await ctx.send(embed=embed)

    else:

        embed=discord.Embed(title="403 Forbidden :(", description="You don't have administrator privileges", color=0xae4dff)
        await ctx.send(embed=embed)


@bot.command(brief='Dev command',description='Dev command')
async def say(ctx, term):
    if ctx.author.id == 538921994645798915:

        await channel_say.send(term)


@bot.command(brief='Dev command',description='Dev command')
async def dm(ctx, user: discord.User, *, message):
    if ctx.author.id == 538921994645798915:

        await user.send(message)


@bot.command(brief='Shows a nice piece of art',description='Scrapes a post from the top 100 posts from the past week in r/art (no nsfw obviously)')
async def art(ctx):

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
    await ctx.send(reddit_post.title)
    await ctx.send(reddit_post.url)
    await ctx.send('Posted by u/'+reddit_post.author.name)
    await ctx.send(str(reddit_post.score)+' upvotes')


@bot.command(brief='Shows a cat picture :D',description='Scrapes a post from the top 100 posts from the past week in r/cats')
async def cat(ctx):

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
    await ctx.send(reddit_post.title)
    await ctx.send(reddit_post.url)
    await ctx.send('Posted by u/'+reddit_post.author.name)
    await ctx.send(str(reddit_post.score)+' upvotes')


@bot.command(brief='Shows top 10 trending news from r/news',description='Scrapes the top 10 posts from the hot feed of r/news')
async def news(ctx):

    subreddit = await reddit.subreddit("news")

    post_list = []

    count = 0
    async for submission in subreddit.hot():
        if count == 10:
            break
        if submission.over_18 == False:
            # post_url = 'https://www.reddit.com'+submission.permalink
            post_list.append(submission)
            count += 1

    num = 0
    embed = discord.Embed()
    embedstr = ''
    for post in post_list:

        num += 1
        redditstr = str(num) + ') [' + post.title + '](' + post.url + ')\n\n'
        embedstr += redditstr

    embed.description = embedstr
    await ctx.channel.send(embed=embed)


# @bot.command()
# async def sp(ctx):
#     # https://cdn.discordapp.com/attachments/745066591443746857/879558411895848960/anime-couples.png

#     with open("posts.txt") as file:

#         lines = file.readlines()
#         await ctx.send(random.choice(lines))


@bot.command(brief='Asks a question',description='Asks a question')
async def truth(ctx):

    with open("assets/truth.txt") as file:

        lines = file.readlines()
        await ctx.send(random.choice(lines))


@bot.command(brief='Dev command',description='Dev command')
async def exec(ctx, *, command):

    if ctx.author.id == 538921994645798915:

        exec(command)

    else:
        await ctx.send("You're not my dev! >:(")
        print(ctx.author, 'attempted to execute:\n', ctx.content)


@bot.command(brief='Returns latency to the server',description='Returns latency to the server in milliseconds')
async def ping(ctx):
    await ctx.send(f'Pong! Latency: {round(bot.latency * 1000, 3)}ms')


@bot.command(brief='Returns a latency graph',description='Returns a latency graph over the past 10 minutes')
async def netgraph(ctx):

    time_since_ping = round(time.time() - time_ping)

    x = np.append(np.arange((len(ping_arr) - 1)*-
                  40, 1, 40) - time_since_ping, 0)
    y = np.append(ping_arr, ping_arr[len(ping_arr) - 1])

    X_ = np.linspace(min(x), max(x), 500)
    X_Y_Spline = make_interp_spline(x, y)
    Y_ = X_Y_Spline(X_)

    plt.plot(X_, Y_, color='red')

    plt.xlim(-600, 0)

    plt.ylim(0, max(Y_)*1.1)

    plt.xlabel('Time')

    plt.ylabel('Milliseconds')

    plt.title('Latency within the last 10 minutes')

    plt.savefig("temp/netgraph.png")

    file = discord.File("temp/netgraph.png")
    embed = discord.Embed()
    embed.set_image(url="attachment://netgraph.png")
    await ctx.send(embed=embed, file=file)
    plt.clf()


@bot.command(brief='Gives a weather report at the location',description='Gives a weather report at the location with temperature, wind speed, humidity, air pressure, and a forecast chart')
async def weather(ctx, *, location):

    owm = OWM('a4348bddc4faa37365b82cee8c3136da')
    mgr = owm.weather_manager()
    # the observation object is a box containing a weather object
    observation = mgr.weather_at_place(location)
    w = observation.weather

    reg = owm.city_id_registry()
    list_of_locations = reg.locations_for(location)

    embedVar = discord.Embed(title="Weather in " + location, color=0xae4dff)

    embedVar.add_field(name="Current Temperature", value=
        str(w.temperature('fahrenheit')['temp']) + ' °F / ' +
        str(w.temperature('celsius')['temp']) + ' °C',
        inline=False)

    embedVar.add_field(name="High", value=
        str(w.temperature('fahrenheit')['temp_max']) + ' °F / ' +
        str(w.temperature('celsius')['temp_max']) + ' °C',
        inline=False)
    
    embedVar.add_field(name="Low", value=
        str(w.temperature('fahrenheit')['temp_min']) + ' °F / ' +
        str(w.temperature('celsius')['temp_min']) + ' °C',
        inline=False)

    embedVar.add_field(name="Feels like", value=
        str(w.temperature('fahrenheit')['feels_like']) + ' °F / ' +
        str(w.temperature('celsius')['feels_like']) + ' °C',
        inline=False)

    embedVar.add_field(name="Wind Speed", value=str(
        w.wind()['speed']) + ' m/s', inline=False)

    embedVar.add_field(name='Humidity', value=str(
        w.humidity) + '%', inline=False)

    embedVar.add_field(name='Air Pressure', value=str(
        w.pressure['press']) + ' hPa', inline=False)

    await ctx.send(embed=embedVar)

    _3h_forecast = mgr.forecast_at_place(location, '3h').forecast
    forecast_temps = np.array([])
    for weather in _3h_forecast:

        forecast_temps = np.append(
            forecast_temps, weather.temperature('fahrenheit')['temp'])

    x = np.arange(3, 121, 3)
    y = forecast_temps

    plt.plot(x, y, color='red')

    plt.xlim(0, 120)

    plt.ylim(min(y)*0.9, max(y)*1.1)

    plt.xlabel('Hours into the future')

    plt.ylabel('Temperature in Fahrenheit(°F)')

    plt.title('3 Hour Interval Forecast at ' + location)

    plt.savefig("temp/forecast.png")

    file = discord.File("temp/forecast.png")
    embed = discord.Embed()
    embed.set_image(url="attachment://forecast.png")
    await ctx.send(embed=embed, file=file)
    plt.clf()


@bot.command(brief='General information and credits',description='General information and credits')
async def info(ctx):
    await ctx.send('**RockyBot v1.4.0**\n' \
        'Hi! I am a multipurpose Discord bot developed by awesomeplaya211#4051!\n' \
        'My source code is available on GitHub by using *$github*!\n' \
        'Use $canon for a story!\n'
        'Credits:\n' \
        '**awesomeplaya211#4051** - Main Dev\n' \
        '**@Banshee-72 on GitHub** - Created $ai and helped vastly with major optimizations\n' \
        '**Numberz#4966** - Made profile picture')


@bot.command(brief='A nice backstory',description='A nice backstory')
async def canon(ctx):
    await ctx.send('RockyBot is cannonicaly a genderless asexual protogen that lives in cyberspace\n' \
        'They enjoy programming and playing games and are *totally* not a virtual projecton of the developer')


@bot.command(brief='Shows my profile picture',description='Shows my profile picture made by Numberz#4966')
async def pfp(ctx):

    file = discord.File("assets/pfp.jpg")
    embed = discord.Embed()
    embed.set_image(url="attachment://pfp.jpg")
    await ctx.send(embed=embed, file=file)


@bot.command(brief='My GitHub Repository',description='My GitHub Repository')
async def github(ctx):

    await ctx.send('https://github.com/awesomeplaya211/RockyBot')


@bot.command(brief='Add me to your server!',description='Add me to your server!')
async def invite(ctx):
    await ctx.send('Add me to your server!')
    await ctx.send('https://discord.com/api/oauth2/authorize?client_id=866481377151156304&permissions=259846044736&scope=applications.commands%20bot')


@bot.command(brief='Flips a coin',description='Flips a coin')
async def flip(ctx):

    if bool(random.randint(0, 1)):
        await ctx.send('Heads')

    else:
        await ctx.send('Tails')


@bot.command(brief='Ask the 8ball a question!',description='Ask the 8ball a question!')
async def ball(ctx):
    await ctx.send(random.choice(_8ball))


@bot.command(brief='Play rock paper scissors!',description='Play rock paper scissors!')
async def rps(ctx, choice):

    if choice == 'rock':
        choice = 0
    if choice == 'paper':
        choice = 1
    if choice == 'scissors':
        choice = 2
    if choice == 'r':
        choice = 0
    if choice == 'p':
        choice = 1
    if choice == 's':
        choice = 2

    rng = random.randint(0, 2)

    if choice-rng == 0:
        await ctx.send('Tie')

    elif choice == 0 and rng == 1:
        await ctx.send('You lost lol')

    elif choice == 1 and rng == 2:
        await ctx.send('You lost lol')

    elif choice == 2 and rng == 0:
        await ctx.send('You lost lol')

    else:
        await ctx.send('I call hacks')


# @bot.event
# async def on_message(ctx):

#     await bot.process_commands(ctx)

#     if ctx.author == bot.user:
#         return

#     message = str(ctx.content).lower()

#     if (message.find("gm") != -1 or message.find('good morning') != -1):
#         await ctx.channel.send('Good morning!')

#     if (message.find("gn") != -1 or message.find('good night') != -1):
#         await ctx.channel.send('Good night!')

#     if (message.find("gg") != -1 or message.find('good game') != -1):
#         await ctx.channel.send('Good game!')


@bot.command(brief='Status check with uptime',description='Status check with uptime')
async def status(ctx):
    t2 = time.time()
    await ctx.send('*Bot Online*')
    string = ('Online for ' +
    str(math.floor((t2-t1)/3600)) + ' hours ' +
    str(math.floor(((t2-t1) % 3600)/60)) + ' minutes ' +
    str(round((t2-t1) % 60, 3)) + ' seconds')
    await ctx.send(string)


@bot.command(brief='Kills bot (Dev command)',description='Kills bot (Dev command)')
async def kill(ctx):

    if ctx.author.id == 538921994645798915:
        await ctx.send('*dies*')

        await bot.close()

    else:
        await ctx.send("You're not my dev! >:(")
        print(ctx.author, 'attempted to kill bot')


# @bot.command()
# # debug
# async def uwu(ctx, text):
#     uwu = text
#     uwuified = ''
#     for i in range(len(uwu)):

#         if uwu[i] == 'you':
#             uwu[i] = 'uwu'

#     for i in uwu:

#         uwuified += str(i) + ' '

#     uwuified.strip()
#     uwuified = uwuify.uwu(uwuified)
#     await ctx.send(uwuified + 'uwu')


@bot.command(brief='Hugs :D',description='Hugs :D')
async def hug(ctx):

    await ctx.send('⊂(・▽・⊂)')


@bot.command(brief='Sets which language Wikipedia $wiki searches through',description='Sets which language Wikipedia $wiki searches through using ISO 639-1 codes')
async def wikilang(ctx, language):

    wikipedia.set_lang(language)
    wiki_lang = 'Language set to ' + wikipedia.languages()[language]

    await ctx.send(wiki_lang)


@bot.command(brief='Searches through Wikipedia for an article that matches the input',description='Searches through Wikipedia for an article that matches the input')
async def wiki(ctx, *, search):

    # IMPORTANT!:  ^^^ asterisk will make the str after command into 1 arg regardless of spaces

    wiki_search_param = search

    # wiki_search_str = '*Searching Wikipedia for ' + wiki_search_param + '*'

    # await ctx.send(wiki_search_str)

    try:

        await ctx.send(wikipedia.page(wikipedia.search(wiki_search_param)[0], auto_suggest=False).url)

    except IndexError:

        await ctx.send('***Did you mean ' + wikipedia.page(wiki_search_param, auto_suggest=True).title + '?***')
        await ctx.send(wikipedia.page(wiki_search_param, auto_suggest=True).url)


@bot.command(brief='Returns a random Wikipedia page',description='Returns a random Wikipedia page')
async def randomwiki(ctx):

    await ctx.send(wikipedia.page(wikipedia.random()).url)


@bot.command(brief='Returns a random fact',description='Returns a random fact')
async def fact(ctx):

    await ctx.send(get_fact())


@bot.command(brief="Try and guess a country's flag!",description="Try and guess a country's flag! Shows a random country flag and try and answer what country it is! Say show answer if you're stuck")
async def flag(ctx):

    country = random.choice(list(vp.iso()))

    await ctx.send(vp.flag_src(country))

    def useless(_ctx):
        return True

    while True:

        action = await bot.wait_for('message',  check=useless)

        if any(i.casefold() == action.content.casefold() for i in vp.iso()[country]):

            await ctx.send(action.author.display_name + ' correctly answered ' + vp.iso_code(country) + '!')

            break

        elif action.content.casefold() == 'show answer':

            await ctx.send('The answer was ' + vp.iso_code(country))

            break


@bot.command(brief='How to play Blackjack',description='How to play Blackjack')
async def blackjackinfo(ctx):

    await ctx.send('*Blackjack* also known as *Twenty-One* or *Vingt-et-un* is the most popular casino game in the world where the objective is to get a value of 21.')
    await ctx.send('Numbered cards are worth their number and face cards (such as J Q K) are worth 10.\nHowever, aces are worth either ***1 or 11 and can be interpreted either way***')
    await ctx.send('Examples of winning combinations of 21 include:\n*A K*\n*A 10*\n*3 5 7 6*\n*A 5 7 8*')
    await ctx.send("The dealer (aka me) first deals out 2 cards to itself and the player.The player's cards are both visible, where the one of the dealer's cards are covered")
    await ctx.send("The player can either 'hit' taking a random card or 'stand' choosing to end their turn and not take anymore cards.\nOnce the player's turn ends, the dealer goes. The dealer must keep on taking cards until it's value is 17 or above.\nWhen it reaches that threshold, it stands and ends its turn.")
    await ctx.send("The game can end if:\nThe player gets 21 (win)\nThe dealer gets 21 (lose)\nThe player goes over 21 (lose)\nThe dealer goes over 21 (win)\nIf the dealer has more value than the player during its turn (lose)\nAt the end of both turns the player has more value than the dealer (win)\nAt the end of both turns the player and the dealer have equal value (tie)")
    await ctx.send('Have fun!')
    await ctx.send('*Note: RockyBot does not support underage gambling, play responsibly*')


@bot.command(brief='Play Blackjack!',description='Play Blackjack!')
async def blackjack(ctx):

    cards = np.array(['A', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K',
                      'A', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K',
                      'A', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K',
                      'A', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K',
                      ])

    value = {
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'J': 10,
        'Q': 10,
        'K': 10,
    }

    def hand_value(hand):

        hand_sum_1 = 0

        hand_sum_11 = 0

        for i in hand:

            if i != 'A':

                hand_sum_1 += value[i]
                hand_sum_11 += value[i]

            if i == 'A':

                hand_sum_1 += 1
                hand_sum_11 += 11

        if hand_sum_1 == hand_sum_11:

            return [hand_sum_1]

        else:

            return [hand_sum_1, hand_sum_11]

    def max_value(hand):

        if len(hand_value(hand)) == 1:

            return hand_value(hand)[0]

        if len(hand_value(hand)) == 2:

            if hand_value(hand)[1] > 21:

                return hand_value(hand)[0]

            else:

                return hand_value(hand)[1]

    def _21check(hand, num):

        if len(hand_value(hand)) == 1:

            if hand_value(hand)[0] < num:

                return 'under'

            if hand_value(hand)[0] == num:

                return str(num)

            if hand_value(hand)[0] > num:

                return 'over'

        if len(hand_value(hand)) == 2:

            if (hand_value(hand)[0] < num and hand_value(hand)[1] < num) and (hand_value(hand)[0] < num and hand_value(hand)[1] > num) and (hand_value(hand)[0] > num and hand_value(hand)[1] < num):

                return 'under'

            if hand_value(hand)[0] == num or hand_value(hand)[1] == num:

                return str(num)

            if hand_value(hand)[0] > num and hand_value(hand)[1] > num:

                return 'over'

    rng = list(np.random.choice(cards, 4, replace=False))

    house = rng[:2]
    house_start = rng[:2]
    house_start[1] = '#'

    player = rng[2:4]

    house_str = 'House: ' + (' '.join(map(str, house_start))) + ' | Value: ?'

    player_str = 'Player: ' + \
        (' '.join(map(str, player))) + ' | Value: ' + str(max_value(player))

    await ctx.send(house_str)
    await ctx.send(player_str)

    if _21check(player, 21) == '21':

        await ctx.send('21! You win!')

    else:

        def is_correct(_ctx):
            return _ctx.author == ctx.author

        while True:

            action = await bot.wait_for('message',  check=is_correct)

            if action.content == '$blackjackexit':

                await ctx.send('Exited Blackjack')

                break

            if action.content == 'hit' or action.content == 'Hit':

                player.append(random.choice(cards))

                house_str = 'House: ' + \
                    (' '.join(map(str, house_start))) + ' | Value: ?'

                player_str = 'Player: ' + \
                    (' '.join(map(str, player))) + \
                    ' | Value: ' + str(max_value(player))

                await ctx.send(house_str)
                await ctx.send(player_str)

                # check if hand is above 21 or not
                if _21check(player, 21) == '21':

                    await ctx.send('21! You win!')

                    break

                if _21check(player, 21) == 'over':

                    await ctx.send('Bust! You lose!')

                    break

            if action.content == 'stand' or action.content == 'Stand':

                house_str = 'House: ' + \
                    (' '.join(map(str, house))) + \
                    ' | Value: ' + str(max_value(house))

                player_str = 'Player: ' + \
                    (' '.join(map(str, player))) + \
                    ' | Value: ' + str(max_value(player))

                await ctx.send(house_str)
                await ctx.send(player_str)
                await ctx.send('---------------')

                if _21check(house, 21) == '21':

                    await ctx.send('21! You lose!')

                    break

                if max_value(player) < max_value(house):

                    await ctx.send('I have more value! You lose!')

                    break

                while _21check(house, 16) != 'over':

                    house.append(random.choice(cards))

                    house_str = 'House: ' + \
                        (' '.join(map(str, house))) + \
                        ' | Value: ' + str(max_value(house))

                    player_str = 'Player: ' + \
                        (' '.join(map(str, player))) + \
                        ' | Value: ' + str(max_value(player))

                    await ctx.send(house_str)
                    await ctx.send(player_str)
                    await ctx.send('---------------')

                    if _21check(house, 21) == '21':

                        await ctx.send('21! You lose!')

                        break

                    elif _21check(house, 21) == 'over':

                        await ctx.send('Bust! You win!')

                        break

                    elif max_value(player) < max_value(house):

                        await ctx.send('I have more value! You lose!')

                        break

                if max_value(player) > max_value(house):

                    await ctx.send('You have more value! You win!')

                    break

                elif max_value(player) == max_value(house):

                    await ctx.send('Equal value! Tie!')

                    break


# bot ideas:
# yell at people if 3 people in a row say 'I' or '.'

# blackjack:
# 2 face up to player
# 1 face up 1 face down to bot
# ace can be both 1 or 11
# face cards are 10
# <= 16 bot takes >= 17 bot stands


t1 = time.time()

bot.loop.create_task(heartbeat())

keep_alive()

bot.run(os.getenv('discordtoken'))
