import discord
import asyncio
import logging
import random
import requests
import os


#token = os.environ['TOKEN']
token = "NjQ5ODAxMTYxNjMyOTA3Mjk0.XeCF8g.VCqmwFO5hHNTYhQIuaCOlaU0yf8" 
client = discord.Client()


@client.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print(client)


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
        await client.send_message(message.channel,
        '```' +
        '!pls help : Prints this help message\n'
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
    if message.content.startswith('!pls roll'):
        tmp = await client.send_message(message.channel, 'rolling die...')
        roll = random.randint(1, 6)
        await client.edit_message(tmp, roll)

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
