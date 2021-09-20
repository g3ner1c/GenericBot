import asyncio
import math
import os
import random
import re
import time

import asyncpraw
import discord
import matplotlib.pyplot as plt
import numpy as np
import uwuify
import wikipedia
from discord import channel, message, player
from discord.ext import commands
from dotenv import load_dotenv
from pyowm.owm import OWM
from randfacts import get_fact
from scipy.interpolate import make_interp_spline
from keep_alive import keep_alive

load_dotenv()

bot = commands.Bot(command_prefix='$')

global channel_say
channel_say = 0

# client = discord.Client()

global time_uwu
time_uwu = time.time()

reddit = asyncpraw.Reddit(
    client_id="MZgXIeYJm5rsrFHm9uWCeA",
    client_secret=os.getenv('reddittoken'),
    user_agent="discord:GenericBot:v1.3.0 (by /u/awesomeplaya211)"
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

def txt_increment(text_file):
    
    file = open(text_file,"r+")
    num = file.readline()
    num = int(num.strip())
    file.truncate(0)
    file.close()
    file = open(text_file,"r+")
    file.write(str((num + 1)))

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
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="VScode for 12,021 years"))
    print('We have logged in as {0.user}'.format(bot))

_8ball = ["Certainly yes", "Definentely Yes", "99.9% chance", "The chances are high", "Most likely", 
    
            "Probably", "23% chance", "Not likely", "Don't count on it", "No way OMEGALUL",

            "Try it out and see!", "Ask again later", "Better not tell you now", 

            "Cannot predict now", "Concentrate and ask again", "¯\_(ツ)_/¯"
        
        
        ]

@bot.command()
async def license(ctx):
    license  = 'Copyright © 2021 awesomeplaya211 & Banshee-72 \n Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: \n The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. \nTHE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'
    await ctx.send('By using the bot you agree to the following license:')
    await ctx.send(license)

@bot.command()
# buggy lmao
async def graphing(ctx, subst, equ):
    mequ = equ
    x = np.linspace(-125, 125, 2501)
    y = []
    for i in range(len(x)):
        value = x[i]
        equ = re.sub('x', str(value), equ)
        equ = equ[2:]
        print(equ)
        try:
            res = eval(equ)
        except:
            res = 'Something Failed'
        y.append(res)
        equ = mequ
    plt.xlim(-125, 125)
    plt.ylim(-25, max(y)*1.1)
    plt.plot(x,y)
    plt.savefig("graph.png")

    file = discord.File("graph.png")
    embed = discord.Embed()
    embed.set_image(url="attachment://graph.png")
    await ctx.send(embed=embed, file=file)
    plt.clf()

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command()
async def say(ctx,term):
    if ctx.author.id == 538921994645798915:

        await channel_say.send(term)

@bot.command()
async def test(ctx):
    await ctx.send(ctx.author)

@bot.command()
async def art(ctx):
    
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
    await ctx.send(reddit_post.title)
    await ctx.send(reddit_post.url)
    await ctx.send('Posted by u/'+reddit_post.author.name)
    await ctx.send(str(reddit_post.score)+' upvotes')

@bot.command()
async def cat(ctx):
        
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
    await ctx.send(reddit_post.title)
    await ctx.send(reddit_post.url)
    await ctx.send('Posted by u/'+reddit_post.author.name)
    await ctx.send(str(reddit_post.score)+' upvotes')


@bot.command()
async def news(ctx):

    txt_increment("stats.txt")
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


@bot.command()
async def sp(ctx):
# https://cdn.discordapp.com/attachments/745066591443746857/879558411895848960/anime-couples.png
    
    with open("posts.txt") as file:

        lines = file.readlines()
        await ctx.send(random.choice(lines))

@bot.command()
async def truth(ctx):
        
    with open("truth.txt") as file:

        lines = file.readlines()
        await ctx.send(random.choice(lines))

# @bot.command()
# async def calc(ctx,equ):
#     await ctx.send(str(eval(equ)))

# too complicated ^

@bot.command()
async def exec(ctx, *, command):

    if ctx.author.id == 538921994645798915:
        
        exec(command)
    
    else:
        await ctx.send("You're not my dev! >:(")
        print(ctx.author, 'attempted to execute:\n', ctx.content)
       
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! Latency: {round(bot.latency * 1000, 3)}ms')
         
@bot.command()
async def netgraph(ctx):
        

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
    await ctx.send(embed=embed, file=file)
    plt.clf()


@bot.command()
async def weather(ctx, *, location):
    txt_increment("stats.txt")
    owm = OWM('a4348bddc4faa37365b82cee8c3136da')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(location)  # the observation object is a box containing a weather object
    w = observation.weather

    reg = owm.city_id_registry()
    list_of_locations = reg.locations_for(location)


    # embedVar = discord.Embed(title="Weather in " + location + ' (Latitude:' + str(list_of_locations[0].lat) + ', Longitude:' + str(list_of_locations[0].lon) + ')', color=0xff3131)

    embedVar = discord.Embed(title="Weather in " + location, color=0xff3131) # <-- color of RockyBot role on ***REMOVED*** Server

    embedVar.add_field(name="Current Temperature", value=str(w.temperature('fahrenheit')['temp']) + ' °F / ' + str(w.temperature('celsius')['temp']) + ' °C', inline=False)
    embedVar.add_field(name="High", value=str(w.temperature('fahrenheit')['temp_max']) + ' °F / ' + str(w.temperature('celsius')['temp_max']) + ' °C', inline=False)
    embedVar.add_field(name="Low", value=str(w.temperature('fahrenheit')['temp_min']) + ' °F / ' + str(w.temperature('celsius')['temp_min']) + ' °C', inline=False)
    embedVar.add_field(name="Feels like", value=str(w.temperature('fahrenheit')['feels_like']) + ' °F / ' + str(w.temperature('celsius')['feels_like']) + ' °C', inline=False)

    embedVar.add_field(name="Wind Speed", value=str(w.wind()['speed']) + ' m/s', inline=False)
    
    embedVar.add_field(name='Humidity', value=str(w.humidity) + '%', inline=False)

    embedVar.add_field(name='Air Pressure', value=str(w.pressure['press']) + ' hPa', inline=False)

    await ctx.send(embed=embedVar)

    _3h_forecast = mgr.forecast_at_place(location, '3h').forecast
    forecast_temps = np.array([])
    for weather in _3h_forecast:

        forecast_temps = np.append(forecast_temps, weather.temperature('fahrenheit')['temp'])


    x = np.arange(3,121,3)
    y = forecast_temps

    plt.plot(x,y, color = 'red')

    plt.xlim(0, 120)

    plt.ylim(min(y)*0.9, max(y)*1.1)

    plt.xlabel('Hours into the future')

    plt.ylabel('Temperature in Fahrenheit(°F)')

    plt.title('3 Hour Interval Forecast at ' + location)

    plt.savefig("forecast.png")




    file = discord.File("forecast.png") # an image in the same folder as the main bot file
    embed = discord.Embed() # any kwargs you want here
    embed.set_image(url="attachment://forecast.png")
    # filename and extension have to match (ex. "thisname.jpg" has to be "attachment://thisname.jpg")
    await ctx.send(embed=embed, file=file)
    plt.clf()



#                               put repo branch in $info here for easier testing
#                                                vvvvvvvv

@bot.command()
async def info(ctx):
    await ctx.send('*RockyBot v1.3.0 - main*\nHi! I am an emotionless bot programmed to feign a personality to you!\nMy owner is awesomeplaya211#4051\nDM him for bug reports or suggestions\nNotable contributions (@Banshee-72 on GitHub)\n**I am now open source!**\n**Use $github for my Github page!**\nProfile picture by Johnny Boy#4966')
        
@bot.command()
async def pfp(ctx):

    file = discord.File("pfp.jpg") # an image in the same folder as the main bot file
    embed = discord.Embed() # any kwargs you want here
    embed.set_image(url="attachment://pfp.jpg")
    # filename and extension have to match (ex. "thisname.jpg" has to be "attachment://thisname.jpg")
    await ctx.send(embed=embed, file=file)

@bot.command()
async def github(ctx):
        
    await ctx.send('https://github.com/awesomeplaya211/RockyBot')

@bot.command()
async def invite(ctx):
    await ctx.send('Add me to your server!')
    await ctx.send('https://discord.com/api/oauth2/authorize?client_id=866481377151156304&permissions=259846044736&scope=applications.commands%20bot')
        
@bot.command()
async def flip(ctx):

    if bool(random.randint(0,1)):
        await ctx.send('Heads')
        

    else:
        await ctx.send('Tails')
            
@bot.command()
async def ball(ctx):
        await ctx.send(random.choice(_8ball))
        
@bot.command()
async def rps(ctx,choice):

    if choice == 'rock': choice = 0
    if choice == 'paper': choice = 1
    if choice == 'scissors': choice = 2
    if choice == 'r': choice = 0
    if choice == 'p': choice = 1
    if choice == 's': choice = 2

    rng = random.randint(0,2)

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
            
       
@bot.event
async def on_message(ctx):

    await bot.process_commands(ctx)

    if ctx.author == bot.user:   
        return

    if (ctx.content.startswith('gm') or ctx.content.startswith('GM') or ctx.content.startswith('good morning') or ctx.content.startswith('Good morning')) and (ctx.content != 'gmas') and (ctx.content != 'GMAS'):

        await ctx.channel.send('Good morning!')
        txt_increment("stats.txt")

    if ctx.content.startswith('gn') or ctx.content.startswith('GN') or ctx.content.startswith('good night') or ctx.content.startswith('Good night'):

       await ctx.channel.send('Good night!')
       txt_increment("stats.txt")

    if ctx.content.startswith('gg') or ctx.content.startswith('GG'):

       await ctx.channel.send('Good game!')
       txt_increment("stats.txt")

    if any(word in ctx.content for word in ['mai san','maisan','MAI SAN','MAISAN','mai-san','Mai-san','MAI-SAN']):   
        file = open("time.txt","r+")
        ltm = float(file.readline().strip())
        now = time.time()
        file.truncate(0)
        file.close()
        file = open("time.txt","r+")
        file.write(str(now))
        if now - ltm > 600:
            string = '*This server has gone ' + str((now - ltm)//86400) + ' days ' + str(((now - ltm)%86400)//3600) + ' hours ' + str(((now - ltm)%3600)//60) + ' minutes '+ str(round((now - ltm)%60)) + ' seconds without mentioning Mai-san*'
            await ctx.channel.send(string)
            print(string)

@bot.command()
async def status(ctx):
    t2 = time.time()
    await ctx.send('*Bot Online*')
    string = 'Online for ' + str(math.floor((t2-t1)/3600)) + ' hours ' + str(math.floor(((t2-t1)%3600)/60)) + ' minutes '+ str(round((t2-t1)%60,3)) + ' seconds'
    await ctx.send(string)
          
@bot.command()
async def hmm(ctx):
    await ctx.send('https://i.pinimg.com/originals/15/8b/ed/158bed9819e4fccf7e18a5eeeaf79c6b.png')
        
@bot.command()
async def kill(ctx):

    if ctx.author.id == 538921994645798915:
        await ctx.send('*dies*')
        
        await bot.close()

    else:
        await ctx.send("You're not my dev! >:(")
        print(ctx.author, 'attempted to kill bot')
            
#@bot.command()
#async def help(ctx):
#        await ctx.send('$info - information about me\n$github - my github page\n$status - bot status\n$invite - add me to your server\n$flip - flips a coin\n$8ball - 100% accurate answer to any question\n$rps - Rock Paper Scissors\n$hmm - hmm\n$kill - kills me **dont do this plz :C**')
#        await ctx.send('$secret - its a secret! >_<\n$uwuify - UWU\n$stats - statistics\n$hug - hugs :D\n$blackjack - play me in blackjack!\n$blackjackstats - blackjack stats!\n$wiki - search wikipedia\n$fact - tell you a random fact\n$ping - latency test\n$netgraph - latency graph\n$art - top 100 post from r/art from the past week\n$cat - top 100 post from r/cats from the past week\n$shitpost or $196 - shitpost generator (sourced from Johnny Boy#4966 and various shitpost subreddits)')
          
@bot.command()
async def secret(ctx):
    await ctx.send('https://media.tenor.com/images/7598d103a735d5568964e4967e42823d/tenor.gif')
    time.sleep(3)
    await ctx.send('lol baited')
          
@bot.command()
async def copycat(ctx):
    await ctx.send(ctx)
          
@bot.command()
#debug
async def uwu(ctx,text):
    uwu  = text
    uwuified = ''
    for i in range(len(uwu)):

        if uwu[i] == 'you':
            uwu[i] = 'uwu'

    for i in uwu:

        uwuified += str(i) + ' '

    uwuified.strip()
    uwuified = uwuify.uwu(uwuified)
    await ctx.send(uwuified + 'uwu')
         
@bot.command()
async def stats(ctx):
    txt_increment("stats.txt")
    file = open("stats.txt","r+")
    stat = file.readline()
    stat = int(stat.strip())
    string_stat = 'I have been called '+ str(stat) + ' times'
    await ctx.send(string_stat)

@bot.command()
async def hug(ctx):

    await ctx.send('⊂(・▽・⊂)')

@bot.command()
async def setlang(ctx,lang):

    wikipedia.set_lang(lang)
    wiki_lang = 'Language set to ' + wikipedia.languages()[lang]

    await ctx.send(wiki_lang)

@bot.command()
async def wiki(ctx, *, search):

    # IMPORTANT!:  ^^^ asterisk will make the str after command into 1 arg regardless of spaces

    wiki_search_param = search

    wiki_search_str = '*Searching Wikipedia for ' + wiki_search_param + '*'

    await ctx.send(wiki_search_str)

    try:

        await ctx.send(wikipedia.page(wikipedia.search(wiki_search_param)[0], auto_suggest = False).url)


    except IndexError:

        await ctx.send('***Did you mean ' + wikipedia.page(wiki_search_param, auto_suggest = True).title + '?***')
        await ctx.send(wikipedia.page(wiki_search_param, auto_suggest = True).url)

@bot.command()
async def randomwiki(ctx):

        
    await ctx.send(wikipedia.page(wikipedia.random()).url)

@bot.command()
async def fact(ctx):

        
    await ctx.send(get_fact())

@bot.command()
async def blackjackinfo(ctx):

    await ctx.send('*Blackjack* also known as *Twenty-One* or *Vingt-et-un* is the most popular casino game in the world where the objective is to get a value of 21.')
    await ctx.send('Numbered cards are worth their number and face cards (such as J Q K) are worth 10.\nHowever, aces are worth either ***1 or 11 and can be interpreted either way***')
    await ctx.send('Examples of winning combinations of 21 include:\n*A K*\n*A 10*\n*3 5 7 6*\n*A 5 7 8*')
    await ctx.send("The dealer (aka me) first deals out 2 cards to itself and the player.The player's cards are both visible, where the one of the dealer's cards are covered")
    await ctx.send("The player can either 'hit' taking a random card or 'stand' choosing to end their turn and not take anymore cards.\nOnce the player's turn ends, the dealer goes. The dealer must keep on taking cards until it's value is 17 or above.\nWhen it reaches that threshold, it stands and ends its turn.")
    await ctx.send("The game can end if:\nThe player gets 21 (win)\nThe dealer gets 21 (lose)\nThe player goes over 21 (lose)\nThe dealer goes over 21 (win)\nIf the dealer has more value than the player during its turn (lose)\nAt the end of both turns the player has more value than the dealer (win)\nAt the end of both turns the player and the dealer have equal value (tie)")
    await ctx.send('Have fun!')
    await ctx.send('*Note: RockyBot does not support underage gambling, play responsibly*')

@bot.command()
async def blackjackstats(ctx):

    file = open("blackjackstats.txt","r+")
    stat = file.readline()
    stat = stat.strip()
    stat = stat.split()
    beat, lost, tied = stat
    string_stat = 'I have beaten ' + beat + ' players, lost to ' + lost + ' players, and tied with ' + tied + ' players'

    await ctx.send(string_stat)

@bot.command()
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


    rng = list(np.random.choice(cards, 4, replace = False))

    house = rng[:2]
    house_start = rng[:2]
    house_start[1] = '#'

    player = rng[2:4]

    house_str = 'House: ' + (' '.join(map(str, house_start))) + ' | Value: ?'

    player_str = 'Player: ' + (' '.join(map(str, player))) + ' | Value: ' + str(max_value(player))

    await ctx.send(house_str)
    await ctx.send(player_str)

    if _21check(player, 21) == '21':

        await ctx.send('21! You win!')
        blackjack_increment("blackjackstats.txt", 1)
        

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
                

                house_str = 'House: ' + (' '.join(map(str, house_start))) + ' | Value: ?'

                player_str = 'Player: ' + (' '.join(map(str, player))) + ' | Value: ' + str(max_value(player))

                await ctx.send(house_str)
                await ctx.send(player_str)
                

                # check if hand is above 21 or not
                if _21check(player, 21) == '21':
                    
                    await ctx.send('21! You win!')
                    blackjack_increment("blackjackstats.txt", 1)
                    
                    break

                if _21check(player, 21) == 'over':
                    
                    await ctx.send('Bust! You lose!')
                    blackjack_increment("blackjackstats.txt", 0)
                    
                    break

            if action.content == 'stand' or action.content == 'Stand':

                
                house_str = 'House: ' + (' '.join(map(str, house))) + ' | Value: ' + str(max_value(house))

                player_str = 'Player: ' + (' '.join(map(str, player))) + ' | Value: ' + str(max_value(player))

                await ctx.send(house_str)
                await ctx.send(player_str)
                await ctx.send('---------------')
                

                if _21check(house, 21) == '21':

                    await ctx.send('21! You lose!')
                    blackjack_increment("blackjackstats.txt", 0)
                    
                    break
                    
                if max_value(player) < max_value(house):

                    await ctx.send('I have more value! You lose!')
                    blackjack_increment("blackjackstats.txt", 0)
                    
                    break

                while _21check(house, 16) != 'over':



                    house.append(random.choice(cards))
                    

                    house_str = 'House: ' + (' '.join(map(str, house))) + ' | Value: ' + str(max_value(house))

                    player_str = 'Player: ' + (' '.join(map(str, player))) + ' | Value: ' + str(max_value(player))

                    await ctx.send(house_str)
                    await ctx.send(player_str)
                    await ctx.send('---------------')


                    if _21check(house, 21) == '21':
                
                        await ctx.send('21! You lose!')
                        blackjack_increment("blackjackstats.txt", 0)
                        
                        break

                    elif _21check(house, 21) == 'over':
                        
                        await ctx.send('Bust! You win!')
                        blackjack_increment("blackjackstats.txt", 1)
                        
                        break

                    elif max_value(player) < max_value(house):

                        await ctx.send('I have more value! You lose!')
                        blackjack_increment("blackjackstats.txt", 0)
                        
                        break

                if max_value(player) > max_value(house):

                    await ctx.send('You have more value! You win!')
                    blackjack_increment("blackjackstats.txt", 1)
                    
                    break
                
                elif max_value(player) == max_value(house):


                    await ctx.send('Equal value! Tie!')
                    blackjack_increment("blackjackstats.txt", 2)
                    
                    break






# bot ideas:
# yell at people if 3 people in a row say 'I' or '.'

# blackjack:
# 2 face up to player
# 1 face up 1 face down to bot
# ace can be both 1 or 11
# face cards are 10
# <= 16 bot takes >= 17 bot stands


# @bot.command(message)
#async def spotify(ctx, user: discord.Member=None):
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

keep_alive()

bot.run(os.getenv('discordtoken'))

# client.get_channel(745066591443746857).send('*System Restart*')
# client.get_channel(745066591443746857).send('*Bot Online*')
