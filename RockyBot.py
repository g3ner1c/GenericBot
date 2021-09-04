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

import features


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





@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="with your mom lmao"))
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

    if msg.startswith('$hello'):
        await features.hello(message)

    if msg.startswith('$idsay'):
        features.idsay(message)

    if msg.startswith('$say'):
        features.say(message)

    if msg.startswith('$flag'):
        features.flag(message)
    
    if msg.startswith('$test'):
        features.test(message)
        
    if msg.startswith('$art'):
        features.art(message)

    if msg.startswith('$cat'):
        features.cat(message)

    if msg.startswith('$196') or msg.startswith('$shitpost'):
        features.sp(message)

    if msg.startswith('$truth'):
        features.truth(message)

    if msg.startswith('$calc'):
        features.calc(message)

    if msg.startswith('$ping'):
        features.ping(message)

    if msg.startswith('$netgraph'):
        features.netgraph(message)

    # non migrated code ahead




    if msg.startswith('$furry'):
        await message.channel.send("Liking Protogen doesn't make me a furry right? RIGHT?")
        txt_increment("stats.txt")




    #                               put repo branch in $info here for easier testing
    #                                                vvvvvvvv

    if msg.startswith('$info'):
        await message.channel.send('*RockyBot v1.2.2 - main*\nHi! I am an emotionless bot programmed to feign a personality to you!\nMy owner is awesomeplaya211#4051\nDM him for bug reports or suggestions\nNotable contributions by NordVPN#1637 (@Banshee-72 on GitHub)\n**I am now open source!**\n**Use $github for my Github page!**\nProfile picture by Johnny Boy#4966')
        txt_increment("stats.txt")


    if msg.startswith('$pfp'):

        file = discord.File("pfp.jpg") # an image in the same folder as the main bot file
        embed = discord.Embed() # any kwargs you want here
        embed.set_image(url="attachment://pfp.jpg")
        # filename and extension have to match (ex. "thisname.jpg" has to be "attachment://thisname.jpg")
        await message.channel.send(embed=embed, file=file)

    if msg.startswith('$github'):
        txt_increment("stats.txt")
        await message.channel.send('https://github.com/awesomeplaya211/RockyBot')


    if msg.startswith('$invite'):
        await message.channel.send('Add me to your server!')
        await message.channel.send('https://discord.com/api/oauth2/authorize?client_id=866481377151156304&permissions=2148002880&scope=bot')
        txt_increment("stats.txt")


    if msg.startswith('$flip'):

        if bool(random.randint(0,1)):
            await message.channel.send('Heads')
            txt_increment("stats.txt")

        else:
            await message.channel.send('Tails')
            txt_increment("stats.txt")

    _8ball = ["Certainly yes", "Definentely Yes", "99.9% chance", "The chances are high", "Most likely", 
    
            "Probably", "23% chance", "Not likely", "Don't count on it", "No way OMEGALUL",

            "Try it out and see!", "Ask again later", "Better not tell you now", 

            "Cannot predict now", "Concentrate and ask again", "¯\_(ツ)_/¯"
        
        
        ]
    
    if msg.startswith('$8ball'):
        await message.channel.send(random.choice(_8ball))
        txt_increment("stats.txt")


    if msg.startswith('$rps'):

        rng = random.randint(0,2)

        if rng == 0:
            await message.channel.send('You win!')
            txt_increment("stats.txt")

        elif rng == 1:
            await message.channel.send('lmao you lost')
            txt_increment("stats.txt")

        else:
            await message.channel.send('Tie! Wanna go again?')
            txt_increment("stats.txt")

    if (msg.startswith('gm') or msg.startswith('GM') or msg.startswith('good morning') or msg.startswith('Good morning')) and (msg != 'gmas') and (msg != 'GMAS'):

        await message.channel.send('Good morning!')
        txt_increment("stats.txt")

    if msg.startswith('gn') or msg.startswith('GN') or msg.startswith('good night') or msg.startswith('Good night'):

       await message.channel.send('Good night!')
       txt_increment("stats.txt")

    if msg.startswith('gg') or msg.startswith('GG'):

       await message.channel.send('Good game!')
       txt_increment("stats.txt")

    # if any(word in msg for word in ['69','420']):
    #     await message.channel.send('nice')

    # if any(word in msg for word in ['owo','OWO','uwu','UWU','oWo','uWu','UwU','OwO']) and message.author.id != 545025575295909899 and not msg.startswith('$uwuify'):
    #     # time_uwu = time.time()
    #     await message.channel.send('uwu')

    # if any(word in msg for word in ['rockybot bad','RockyBot bad','rockybot Bad','Rockybot Bad','rockybot is bad','RockyBot is bad', 'Rockybot is bad']):
    #     await message.channel.send('I will come to your house and murder you in your sleep :)')



    if any(word in msg for word in ['mai san','maisan','MAI SAN','MAISAN','mai-san','Mai-san','MAI-SAN']):
        
        txt_increment("stats.txt")
        file = open("time.txt","r+")
        ltm = float(file.readline().strip())
        now = time.time()
        file.truncate(0)
        file.close()
        file = open("time.txt","r+")
        file.write(str(now))
        if now - ltm > 600:
            string = '*This server has gone ' + str((now - ltm)//86400) + ' days ' + str(((now - ltm)%86400)//3600) + ' hours ' + str(((now - ltm)%3600)//60) + ' minutes '+ str(round((now - ltm)%60)) + ' seconds without mentioning Mai-san*'
            await message.channel.send(string)
            print(string)



    if msg.startswith('$status'):
        t2 = time.time()
        await message.channel.send('*Bot Online*')
        string = 'Online for ' + str(math.floor((t2-t1)/3600)) + ' hours ' + str(math.floor(((t2-t1)%3600)/60)) + ' minutes '+ str(round((t2-t1)%60,3)) + ' seconds'
        await message.channel.send(string)
        txt_increment("stats.txt")
    
    if msg.startswith('$hmm'):
        await message.channel.send('https://i.pinimg.com/originals/15/8b/ed/158bed9819e4fccf7e18a5eeeaf79c6b.png')
        txt_increment("stats.txt")

    if msg.startswith('$kill'):

        if message.author.id == 538921994645798915:
            await message.channel.send('*dies*')
            txt_increment("stats.txt")
            await client.logout()

        else:
            await message.channel.send("You're not my dev! >:(")
            print(message.author, 'attempted to kill bot')
            txt_increment("stats.txt")




    if msg.startswith('$help'):
        await message.channel.send('$info - information about me\n$github - my github page\n$status - bot status\n$invite - add me to your server\n$flip - flips a coin\n$8ball - 100% accurate answer to any question\n$rps - Rock Paper Scissors\n$hmm - hmm\n$kill - kills me **dont do this plz :C**')
        await message.channel.send('$secret - its a secret! >_<\n$uwuify - UWU\n$stats - statistics\n$hug - hugs :D\n$blackjack - play me in blackjack!\n$blackjackstats - blackjack stats!\n$wiki - search wikipedia\n$fact - tell you a random fact\n$ping - latency test\n$netgraph - latency graph\n$art - top 100 post from r/art from the past week\n$cat - top 100 post from r/cats from the past week\n$shitpost or $196 - shitpost generator (sourced from Johnny Boy#4966 and various shitpost subreddits)')
        txt_increment("stats.txt")
    
    if msg.startswith('$secret'):
        await message.channel.send('https://media.tenor.com/images/7598d103a735d5568964e4967e42823d/tenor.gif')
        await message.channel.send('lmao baited')
        txt_increment("stats.txt")
    
    if msg.startswith('$copycat'):
        await message.channel.send(msg)
        txt_increment("stats.txt")
    
    if msg.startswith('$uwuify'):
        uwu = msg
        uwu = uwu.split()
        uwu.remove('$uwuify')
        uwuified = ''
        for i in range(len(uwu)):

            if uwu[i] == 'you':
                uwu[i] = 'uwu'

        for i in uwu:

            uwuified += str(i) + ' '

        uwuified.strip()
        uwuified = uwuify.uwu(uwuified)
        await message.channel.send(uwuified + 'uwu')
        txt_increment("stats.txt")
    
    if msg.startswith('$stats'):

        txt_increment("stats.txt")

        file = open("stats.txt","r+")
        stat = file.readline()
        stat = int(stat.strip())
        string_stat = 'I have been called '+ str(stat) + ' times'
        await message.channel.send(string_stat)

    if msg.startswith('$hug'):

        await message.channel.send('⊂(・▽・⊂)')

    if msg.startswith('$lenny'):

        await message.channel.send('( ͡° ͜ʖ ͡°)')



    if msg.startswith('$setwikilang'):

        txt_increment("stats.txt")

        wiki_lang = msg
        wiki_lang = wiki_lang.split()
        wikipedia.set_lang(wiki_lang[1])
        wiki_lang = 'Language set to ' + wikipedia.languages()[wiki_lang[1]]

        await message.channel.send(wiki_lang)

    if msg.startswith('$wiki'):

        txt_increment("stats.txt")

        wiki_search = msg
        wiki_search = wiki_search.split()
        wiki_search.remove('$wiki')
        wiki_search_param = ''

        for i in wiki_search:

            wiki_search_param += i + ' '

        wiki_search_param = wiki_search_param.strip()

        wiki_search_str = '*Searching Wikipedia for ' + wiki_search_param + '*'

        await message.channel.send(wiki_search_str)

        try:

            await message.channel.send(wikipedia.page(wikipedia.search(wiki_search_param)[0], auto_suggest = False).url)


        except IndexError:

            await message.channel.send('***Did you mean ' + wikipedia.page(wiki_search_param, auto_suggest = True).title + '?***')
            await message.channel.send(wikipedia.page(wiki_search_param, auto_suggest = True).url)

    if msg.startswith('$randomwikipage'):

        txt_increment("stats.txt")
        await message.channel.send(wikipedia.page(wikipedia.random()).url)

    if msg.startswith('$fact'):

        txt_increment("stats.txt")
        await message.channel.send(get_fact())



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

        await message.channel.send('*Blackjack* also known as *Twenty-One* or *Vingt-et-un* is the most popular casino game in the world where the objective is to get a value of 21.')
        await message.channel.send('Numbered cards are worth their number and face cards (such as J Q K) are worth 10.\nHowever, aces are worth either ***1 or 11 and can be interpreted either way***')
        await message.channel.send('Examples of winning combinations of 21 include:\n*A K*\n*A 10*\n*3 5 7 6*\n*A 5 7 8*')
        await message.channel.send("The dealer (aka me) first deals out 2 cards to itself and the player.The player's cards are both visible, where the one of the dealer's cards are covered")
        await message.channel.send("The player can either 'hit' taking a random card or 'stand' choosing to end their turn and not take anymore cards.\nOnce the player's turn ends, the dealer goes. The dealer must keep on taking cards until it's value is 17 or above.\nWhen it reaches that threshold, it stands and ends its turn.")
        await message.channel.send("The game can end if:\nThe player gets 21 (win)\nThe dealer gets 21 (lose)\nThe player goes over 21 (lose)\nThe dealer goes over 21 (win)\nIf the dealer has more value than the player during its turn (lose)\nAt the end of both turns the player has more value than the dealer (win)\nAt the end of both turns the player and the dealer have equal value (tie)")
        await message.channel.send('Have fun!')
        await message.channel.send('*Note: RockyBot does not support underage gambling, play responsibly*')

    if msg == '$blackjackstats':

        file = open("blackjackstats.txt","r+")
        stat = file.readline()
        stat = stat.strip()
        stat = stat.split()
        beat, lost, tied = stat
        string_stat = 'I have beaten ' + beat + ' players, lost to ' + lost + ' players, and tied with ' + tied + ' players'

        await message.channel.send(string_stat)


    if msg == '$blackjack': 

        txt_increment("stats.txt")
        
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

        await message.channel.send(house_str)
        await message.channel.send(player_str)

        if _21check(player, 21) == '21':

            await message.channel.send('21! You win!')
            blackjack_increment("blackjackstats.txt", 1)
            txt_increment("stats.txt")

        else:
    
            def is_correct(_msg):
                return _msg.author == message.author

            while True:

                action = await client.wait_for('message',  check=is_correct)

                if action.content == '$blackjackexit':
                    
                    await message.channel.send('Exited Blackjack')
                    txt_increment("stats.txt")
                    break 

                if action.content == 'hit' or action.content == 'Hit':

                    player.append(random.choice(cards))
                    txt_increment("stats.txt")

                    house_str = 'House: ' + (' '.join(map(str, house_start))) + ' | Value: ?'

                    player_str = 'Player: ' + (' '.join(map(str, player))) + ' | Value: ' + str(max_value(player))

                    await message.channel.send(house_str)
                    await message.channel.send(player_str)
                    

                    # check if hand is above 21 or not
                    if _21check(player, 21) == '21':
                        
                        await message.channel.send('21! You win!')
                        blackjack_increment("blackjackstats.txt", 1)
                        txt_increment("stats.txt")
                        break

                    if _21check(player, 21) == 'over':
                        
                        await message.channel.send('Bust! You lose!')
                        blackjack_increment("blackjackstats.txt", 0)
                        txt_increment("stats.txt")
                        break

                if action.content == 'stand' or action.content == 'Stand':

                    txt_increment("stats.txt")
                    house_str = 'House: ' + (' '.join(map(str, house))) + ' | Value: ' + str(max_value(house))

                    player_str = 'Player: ' + (' '.join(map(str, player))) + ' | Value: ' + str(max_value(player))

                    await message.channel.send(house_str)
                    await message.channel.send(player_str)
                    await message.channel.send('---------------')
                    

                    if _21check(house, 21) == '21':

                        await message.channel.send('21! You lose!')
                        blackjack_increment("blackjackstats.txt", 0)
                        txt_increment("stats.txt")
                        break
                        
                    if max_value(player) < max_value(house):

                        await message.channel.send('I have more value! You lose!')
                        blackjack_increment("blackjackstats.txt", 0)
                        txt_increment("stats.txt")
                        break

                    while _21check(house, 16) != 'over':



                        house.append(random.choice(cards))
                        txt_increment("stats.txt")

                        house_str = 'House: ' + (' '.join(map(str, house))) + ' | Value: ' + str(max_value(house))

                        player_str = 'Player: ' + (' '.join(map(str, player))) + ' | Value: ' + str(max_value(player))

                        await message.channel.send(house_str)
                        await message.channel.send(player_str)
                        await message.channel.send('---------------')


                        if _21check(house, 21) == '21':
                    
                            await message.channel.send('21! You lose!')
                            blackjack_increment("blackjackstats.txt", 0)
                            txt_increment("stats.txt")
                            break

                        elif _21check(house, 21) == 'over':
                            
                            await message.channel.send('Bust! You win!')
                            blackjack_increment("blackjackstats.txt", 1)
                            txt_increment("stats.txt")
                            break

                        elif max_value(player) < max_value(house):

                            await message.channel.send('I have more value! You lose!')
                            blackjack_increment("blackjackstats.txt", 0)
                            txt_increment("stats.txt")
                            break

                    if max_value(player) > max_value(house):

                        await message.channel.send('You have more value! You win!')
                        blackjack_increment("blackjackstats.txt", 1)
                        txt_increment("stats.txt")
                        break
                    
                    elif max_value(player) == max_value(house):


                        await message.channel.send('Equal value! Tie!')
                        blackjack_increment("blackjackstats.txt", 2)
                        txt_increment("stats.txt")
                        break

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
