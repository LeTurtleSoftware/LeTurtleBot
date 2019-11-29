import discord
import asyncio
import logging
import random
import requests
import os
import sys
import time
import os


import os
import psycopg2

try:
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    token = os.environ['TOKEN']
    channel_id = int(os.environ['CHANNEL_ID'])

except Exception as E:
    print("Local Execution")
    token = sys.argv[1]
    DATABASE_URL = sys.argv[2]
    channel_id = int(sys.argv[3])

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()


client = discord.Client()


@client.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print(client)


    cur.execute("""SELECT EXISTS(
        SELECT * 
        FROM information_schema.tables 
        WHERE 
        table_name = 'trappers'
    );""")
    existence = cur.fetchone()[0]
    if not existence:
        cur.execute("""CREATE TABLE trappers(
                        user_id INTEGER PRIMARY KEY,
                        username VARCHAR (50) UNIQUE NOT NULL,
                        traps INTEGER NOT NULL
                        );"""
                    )
        conn.commit()


"""async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n")

            await asyncio.sleep(5)
        except Exception as e:
            print(e)
            await asyncio.sleep(5)
"""

'''
@client.event
async def on_member_join(member):
    global joined
    joined += 1
    for channel in member.server.channels:
        if str(channel) == "general":
            await client.send_message(f"""Welcome to the server {member.mention}""")
'''

@client.event
async def on_message(message):
    id = client.get_guild(channel_id)
    if message.content.startswith('!pls help'):  # make sure to update this with new commands as they are added
        await message.channel.send(message.channel,
        '```' +
        '!pls hola : Saludo agradable para personas agradables (ping)\n'
        '!pls roll : Roll a die\n'
        '!pls flip : Flip a coin'
        '!pls cat  : Finds a cute cat'
        '```')

        # unlisted commands:
        # ]catgif, sometimes fails
        # ]eval, can be used to dump internal variables to Discord
        # ]game, sets the bot's playing status

    if message.content.find("bbtraps") != -1:
        nombre = str(message.author).split("#")[0]
        user_id = str(message.author).split("#")[1]
        print("Alguien esta pidiendo traps -> {}".format(nombre))
        cur.execute("SELECT * FROM trappers WHERE username = '{}';".format(nombre))
        user = cur.fetchone()
        print(user)
        if not user:
            cur.execute("INSERT INTO trappers (user_id, username, traps) VALUES ({}, '{}', {})".format(user_id, nombre, 1))
            conn.commit()
            print("Nuevo Trapero")
        else:
            traps = user[2] + 1
            cur.execute("UPDATE trappers SET traps = {} WHERE user_id = {}".format(traps, user_id))
            conn.commit()
            print("Trapero Old School")

    #TODO: Any Hetero Request is a -1 in Trap Rank

    if message.content.find("!pls hola") != -1:
        nombre = str(message.author).split("#")[0]
        await message.channel.send("A ver que es la joda perro catrehijueputa, aprenda a manejar perro jijueputa {}".format(nombre)) 

    elif message.content == "!pls trapleader":
        embed=discord.Embed(title="Trap Masters Top 10", description="Ranking de adictos a los traps ", color=0xff80ff)
        cur.execute("SELECT * FROM trappers ORDER BY traps DESC LIMIT 10")
        leadership = cur.fetchall()
        message_str = '.\n******************************\n'
        for trapper in leadership:
            embed.add_field(name=trapper[1], value=trapper[2], inline=False)
        await message.channel.send(embed=embed)


#client.loop.create_task(update_stats())
client.run(token)



"""
@client.event
async def on_message(message):

    # Logs server activity to terminal
    print(str(message.author) + ' @ ' + str(message.channel) + ' : ' + message.content)

    # ping th bot and it pongs back!
    if message.content.startswith('!pls ping'):
        await message.channel.send('I heard you! {0.name}'.format(message.author))
        #await client.send_message(message.channel, message.author.mention + ' pong!')

    # prints a helpful message
    if message.content.startswith('!pls help'):  # make sure to update this with new commands as they are added
        await message.channel.send(message.channel,
        '```' +
        '!pls TrapMaster : Prints this help message\n'
        '!pls ping : Ping me and I will pong you back!\n'
        '!pls roll : Roll a die\n'
        '!pls flip : Flip a coin'
        '!pls cat  : Finds a cute cat'
        '```')

        # unlisted commands:
        # ]catgif, sometimes fails
        # ]eval, can be used to dump internal variables to Discord
        # ]game, sets the bot's playing status

    # coinflip, flips a coin
    if message.content.startswith(('!pls coinflip', '!pls flip')):
        tmp = await client.send_message(message.channel, 'flipping coin...')
        flip = random.randint(0, 1)
        if flip == 0:
            await client.edit_message(tmp, 'tails')
        else:
            await client.edit_message(tmp, 'heads')

    # die roll
    if message.content.startswith('!pls count'):
        counter = 0
        repeat = 0
        for x in range(0, 4): # Repeats 4 times
            async for msg in client.logs_from(message.channel, limit=500):
                if msg.author == message.author:
                    counter += 1
            repeat += 1
        await client.send_message(message.channel, "{} has {} out of the first {} messages in {}".format(message.author, str(counter), 500*repeat, message.channel))

    # no Discord bot is complete without the ability to find cats, courtesy of theCatApi
    if message.content.startswith('!pls catgif'):
            # output a cat picture
            await client.send_message(message.channel, requests.get('http://thecatapi.com/api/images/get?format=src&type=gif').url + ' :cat:')
    elif message.content.startswith('!pls cat'):
            # output a cat picture
            await client.send_message(message.channel, requests.get('http://thecatapi.com/api/images/get?format=src&type=jpg').url + ' :cat:')

    # can spit out internal variables into Discord, sometimes useful
    if message.content.lower().startswith('!pls eval '):
        if str(message.author) == owner:
            await client.send_message(message.channel, eval(message.content[6:]))
        else:
            await client.send_message(message.channel, 'you do not have permission to do that')

    # for setting the playing status
    if message.content.lower().startswith('!pls game '):
        if str(message.author) == owner:
            await client.change_presence(game=discord.Game(name=message.content[6:]))
        else:
            await client.send_message(message.channel, 'you do not have permission to do that')

    # self explanatory
    if message.content.lower().startswith(('!pls whoisagoodbot', '!pls whoisthebestbot')):
        await client.send_message(message.channel, 'I am!')

client.run(token)
"""