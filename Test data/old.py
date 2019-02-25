import discord
import asyncio
import requests
import re
from hackerrank.HackerRankAPI import HackerRankAPI

HACKERRANK_API_KEY = 'hackerrank|3491785-2301|18ff1e697a4f9435ceba9e9c87f01ad8d1bfc854'
DISCORD_API_KEY = 'MzYxNDI2NjMxNjIzMDQ5MjE2.D1D53w.zvCrlUmNIjEclBk74V_rFHe2YY0'

compiler = HackerRankAPI(api_key = HACKERRANK_API_KEY)
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    # example commands
    # if message.content.startswith('!test'):
    #     counter = 0
    #     tmp = await client.send_message(message.channel, 'Calculating messages...')
    #     async for log in client.logs_from(message.channel, limit=100):
    #         if log.author == message.author:
    #             counter += 1
    #
    #     await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    # elif message.content.startswith('!sleep'):
    #     await asyncio.sleep(5)
    #     await client.send_message(message.channel, 'Done sleeping')
    if re.search('`.*`.*', message.content):
        command =  message.content.split('`')[1].split()
        inputs = message.content.split('`')[2].split()
        if command[0] == 'compile':
            if command[1] == 'file':
                print('Checking for attachment...\n')
                if len(message.attachments):
                    url = message.attachments[0]['url']
                    print('Getting file from URL:\n' + url + '\n')
                    r = requests.get(url)
                    source = r.text
                    print(source)
                    result = compiler.run({
                        'source': source,
                        'lang': command[2],
                        'testcases': ["hello"]
                        })
                    print(result.output)
            elif command[1] == 'block':
                print('Compiling block')
            else:
                client.send_message(message.channel, 'Sorry, I do not know how to compile that. :)')


client.run(DISCORD_API_KEY)
