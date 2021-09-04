import asyncio
import json
import math
import os
import random
import re
import time
import re
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


#TODO Create translate feature
#TODO Create read feature
#TODO Create help feature


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
    global auth
    auth  = []
    global channel_say
    channel_say = 0

    async def help(message):
        license  = 'Copyright © 2021 awesomeplaya211 & Banshee-72 \n Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: \n The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. \nTHE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'
        await message.channel.send('By using the bot you agree to the following license:')
        await message.channel.send(license)
        with open('auth.pckl', 'rb') as file:
            auth = pickle.load(file)
        auth = auth
        with open('auth.pckl', 'wb') as file:
            auth.append(message.author)
            auth = pickle.dump(auth,file)
        with open('help.pckl', 'rb') as file:
            pages = pickle.load(file)
        page = message.content[-1:]
        try:
            if pages[page]:
                await message.channel.send(pages[page])
        except:
            await message.channel.send('lol it broke')



    _8ball = ["Certainly yes", "Definentely Yes", "99.9% chance", "The chances are high", "Most likely", 
    
            "Probably", "23% chance", "Not likely", "Don't count on it", "No way OMEGALUL",

            "Try it out and see!", "Ask again later", "Better not tell you now", 

            "Cannot predict now", "Concentrate and ask again", "¯\_(ツ)_/¯"
        
        
        ]

    async def graphing(message):

        msg = message.content
        equ = msg[6:]
        equ = equ.strip(' ')
        equ = equ
        equ = equ[:len(equ)-2]
        subst = equ[::-1][0]
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

        # you forgot plt.savefig() - awesomeplaya211

        plt.savefig("graph.png")

        file = discord.File("graph.png")
        embed = discord.Embed()
        embed.set_image(url="attachment://graph.png")
        await message.channel.send(embed=embed, file=file)
        plt.clf()
        
    async def hello(message):
        await message.channel.send('Hello!')
        
    async def idsay(message):
        
        if message.author.id == 538921994645798915:

            channel_say = client.get_channel(int(message.content[7:]))
            print('channel_say set to '+ message.content[7:])

    async def say(message):

        
        if message.author.id == 538921994645798915:

            await channel_say.send(message.content[5:])
    
    async def test(message):
        await message.channel.send(message.author)
        
    async def art(message):
        
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
            
            with open("posts.txt") as file:

                lines = file.readlines()
                await message.channel.send(random.choice(lines))

        async def truth():
            
            with open("truth.txt") as file:

                lines = file.readlines()
                await message.channel.send(random.choice(lines))

    async def truth(message):
        
        with open("truth.txt") as file:

            lines = file.readlines()
            await message.channel.send(random.choice(lines))

    async def calc(message):


        
        await message.channel.send(str(eval(message.content[6:])))
       
    async def ping(message):
        await message.channel.send(f'Pong! Latency: {round(client.latency * 1000, 3)}ms')
         
    async def netgraph(message):
        

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

    #                               put repo branch in $info here for easier testing
    #                                                vvvvvvvv

    async def info(message):
        await message.channel.send('*RockyBot v1.2.2 - dev*\nHi! I am an emotionless bot programmed to feign a personality to you!\nMy owner is awesomeplaya211#4051\nDM him for bug reports or suggestions\nNotable contributions (@Banshee-72 on GitHub)\n**I am now open source!**\n**Use $github for my Github page!**\nProfile picture by Johnny Boy#4966')
        
    async def pfp(message):

        file = discord.File("pfp.jpg") # an image in the same folder as the main bot file
        embed = discord.Embed() # any kwargs you want here
        embed.set_image(url="attachment://pfp.jpg")
        # filename and extension have to match (ex. "thisname.jpg" has to be "attachment://thisname.jpg")
        await message.channel.send(embed=embed, file=file)

    async def github(message):
        
        await message.channel.send('https://github.com/awesomeplaya211/RockyBot')

    async def invite(message):
        await message.channel.send('Add me to your server!')
        await message.channel.send('https://discord.com/api/oauth2/authorize?client_id=866481377151156304&permissions=2148002880&scope=bot')
        
    async def flip(message):

        if bool(random.randint(0,1)):
            await message.channel.send('Heads')
            

        else:
            await message.channel.send('Tails')
            
    async def ball(message):
        await message.channel.send(random.choice(Feature._8ball))
        
    async def rps(message):

        rng = random.randint(0,2)

        if rng == 0:
            await message.channel.send('You win!')
            

        elif rng == 1:
            await message.channel.send('lol you lost')
            

        else:
            await message.channel.send('Tie! Wanna go again?')
            
    async def gm(message):

        await message.channel.send('Good morning!')
        
    async def gn(message):

       await message.channel.send('Good night!')
       
    async def gg(message):

       await message.channel.send('Good game!')
       
    async def mai(message):
        
        
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

    async def status(message, t1):
        t2 = time.time()
        await message.channel.send('*Bot Online*')
        string = 'Online for ' + str(math.floor((t2-t1)/3600)) + ' hours ' + str(math.floor(((t2-t1)%3600)/60)) + ' minutes '+ str(round((t2-t1)%60,3)) + ' seconds'
        await message.channel.send(string)
          
    async def hmm(message):
        await message.channel.send('https://i.pinimg.com/originals/15/8b/ed/158bed9819e4fccf7e18a5eeeaf79c6b.png')
        
    async def kill(message):

        if message.author.id == 538921994645798915:
            await message.channel.send('*dies*')
            
            await client.logout()

        else:
            await message.channel.send("You're not my dev! >:(")
            print(message.author, 'attempted to kill bot')
            
#    async def help(message):
#        await message.channel.send('$info - information about me\n$github - my github page\n$status - bot status\n$invite - add me to your server\n$flip - flips a coin\n$8ball - 100% accurate answer to any question\n$rps - Rock Paper Scissors\n$hmm - hmm\n$kill - kills me **dont do this plz :C**')
#        await message.channel.send('$secret - its a secret! >_<\n$uwuify - UWU\n$stats - statistics\n$hug - hugs :D\n$blackjack - play me in blackjack!\n$blackjackstats - blackjack stats!\n$wiki - search wikipedia\n$fact - tell you a random fact\n$ping - latency test\n$netgraph - latency graph\n$art - top 100 post from r/art from the past week\n$cat - top 100 post from r/cats from the past week\n$shitpost or $196 - shitpost generator (sourced from Johnny Boy#4966 and various shitpost subreddits)')
          
    async def secret(message):
        await message.channel.send('https://media.tenor.com/images/7598d103a735d5568964e4967e42823d/tenor.gif')
        await message.channel.send('lol baited')
          
    async def copycat(message):
        await message.channel.send(message.content)
          
    async def uwu(message):
        uwu = message.content
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
         
    async def stats(message):

        

        file = open("stats.txt","r+")
        stat = file.readline()
        stat = int(stat.strip())
        string_stat = 'I have been called '+ str(stat) + ' times'
        await message.channel.send(string_stat)

    async def hug(message):

        await message.channel.send('⊂(・▽・⊂)')

    async def setlang(message):

        wiki_lang = message.content
        wiki_lang = wiki_lang.split()
        wikipedia.set_lang(wiki_lang[1])
        wiki_lang = 'Language set to ' + wikipedia.languages()[wiki_lang[1]]

        await message.channel.send(wiki_lang)

    async def wiki(message):

        

        wiki_search = message.content
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

    async def randomwiki(message):

        
        await message.channel.send(wikipedia.page(wikipedia.random()).url)

    async def fact(message):

        
        await message.channel.send(get_fact())

    async def blackjackinfo(message):

        await message.channel.send('*Blackjack* also known as *Twenty-One* or *Vingt-et-un* is the most popular casino game in the world where the objective is to get a value of 21.')
        await message.channel.send('Numbered cards are worth their number and face cards (such as J Q K) are worth 10.\nHowever, aces are worth either ***1 or 11 and can be interpreted either way***')
        await message.channel.send('Examples of winning combinations of 21 include:\n*A K*\n*A 10*\n*3 5 7 6*\n*A 5 7 8*')
        await message.channel.send("The dealer (aka me) first deals out 2 cards to itself and the player.The player's cards are both visible, where the one of the dealer's cards are covered")
        await message.channel.send("The player can either 'hit' taking a random card or 'stand' choosing to end their turn and not take anymore cards.\nOnce the player's turn ends, the dealer goes. The dealer must keep on taking cards until it's value is 17 or above.\nWhen it reaches that threshold, it stands and ends its turn.")
        await message.channel.send("The game can end if:\nThe player gets 21 (win)\nThe dealer gets 21 (lose)\nThe player goes over 21 (lose)\nThe dealer goes over 21 (win)\nIf the dealer has more value than the player during its turn (lose)\nAt the end of both turns the player has more value than the dealer (win)\nAt the end of both turns the player and the dealer have equal value (tie)")
        await message.channel.send('Have fun!')
        await message.channel.send('*Note: RockyBot does not support underage gambling, play responsibly*')

    async def blackjackstats(message):

        file = open("blackjackstats.txt","r+")
        stat = file.readline()
        stat = stat.strip()
        stat = stat.split()
        beat, lost, tied = stat
        string_stat = 'I have beaten ' + beat + ' players, lost to ' + lost + ' players, and tied with ' + tied + ' players'

        await message.channel.send(string_stat)

    async def blackjack(message): 

        
        
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
            

        else:
    
            def is_correct(_msg):
                return _msg.author == message.author

            while True:

                action = await client.wait_for('message',  check=is_correct)

                if action.content == '$blackjackexit':
                    
                    await message.channel.send('Exited Blackjack')
                    
                    break 

                if action.content == 'hit' or action.content == 'Hit':

                    player.append(random.choice(cards))
                    

                    house_str = 'House: ' + (' '.join(map(str, house_start))) + ' | Value: ?'

                    player_str = 'Player: ' + (' '.join(map(str, player))) + ' | Value: ' + str(max_value(player))

                    await message.channel.send(house_str)
                    await message.channel.send(player_str)
                    

                    # check if hand is above 21 or not
                    if _21check(player, 21) == '21':
                        
                        await message.channel.send('21! You win!')
                        blackjack_increment("blackjackstats.txt", 1)
                        
                        break

                    if _21check(player, 21) == 'over':
                        
                        await message.channel.send('Bust! You lose!')
                        blackjack_increment("blackjackstats.txt", 0)
                        
                        break

                if action.content == 'stand' or action.content == 'Stand':

                    
                    house_str = 'House: ' + (' '.join(map(str, house))) + ' | Value: ' + str(max_value(house))

                    player_str = 'Player: ' + (' '.join(map(str, player))) + ' | Value: ' + str(max_value(player))

                    await message.channel.send(house_str)
                    await message.channel.send(player_str)
                    await message.channel.send('---------------')
                    

                    if _21check(house, 21) == '21':

                        await message.channel.send('21! You lose!')
                        blackjack_increment("blackjackstats.txt", 0)
                        
                        break
                        
                    if max_value(player) < max_value(house):

                        await message.channel.send('I have more value! You lose!')
                        blackjack_increment("blackjackstats.txt", 0)
                        
                        break

                    while _21check(house, 16) != 'over':



                        house.append(random.choice(cards))
                        

                        house_str = 'House: ' + (' '.join(map(str, house))) + ' | Value: ' + str(max_value(house))

                        player_str = 'Player: ' + (' '.join(map(str, player))) + ' | Value: ' + str(max_value(player))

                        await message.channel.send(house_str)
                        await message.channel.send(player_str)
                        await message.channel.send('---------------')


                        if _21check(house, 21) == '21':
                    
                            await message.channel.send('21! You lose!')
                            blackjack_increment("blackjackstats.txt", 0)
                            
                            break

                        elif _21check(house, 21) == 'over':
                            
                            await message.channel.send('Bust! You win!')
                            blackjack_increment("blackjackstats.txt", 1)
                            
                            break

                        elif max_value(player) < max_value(house):

                            await message.channel.send('I have more value! You lose!')
                            blackjack_increment("blackjackstats.txt", 0)
                            
                            break

                    if max_value(player) > max_value(house):

                        await message.channel.send('You have more value! You win!')
                        blackjack_increment("blackjackstats.txt", 1)
                        
                        break
                    
                    elif max_value(player) == max_value(house):


                        await message.channel.send('Equal value! Tie!')
                        blackjack_increment("blackjackstats.txt", 2)
                        
                        break
