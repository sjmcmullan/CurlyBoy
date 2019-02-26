import discord
import asyncio
# import requests
import re
import time
import Commands
from random import randint
import sqlite3
import ApiKey
DISCORD_API_KEY = ApiKey.DISCORD_API_KEY
REMINDER_POLL_CHECK = 60

client = discord.Client()
log_file = open("debugging.log", "a+")
database = sqlite3.connect('database.db')

killcode = "".join([chr(x) for x in [randint(97, 122) for i in range(5)]])

def log_to_file(content):
    #nothin
    return

async def reminder_check():
    await client.wait_until_ready()
    c = database.cursor()
    while not client.is_closed:
        c.execute('''SELECT * FROM reminders WHERE time_end=?''', (time.strftime("%d-%m-%Y-%H:%M"),))
        results = c.fetchall()
        if len(results) >= 1:
            for result in results:
                if result[5] == 1:
                    channel = client.get_channel(result[4])
                    if channel:
                        await client.send_message(channel, result[6])
                elif result[5] == 0:
                    remindee = await client.get_user_info(result[3])
                    if remindee:
                        await client.send_message(remindee, result[6])
        await asyncio.sleep(REMINDER_POLL_CHECK) # task runs every x seconds


async def flash_message(channel, message, length):
    flashed_message = await client.send_message(channel, message)
    await asyncio.sleep(length)
    await client.delete_message(flashed_message)
    return


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('---------------------------')
    print("KILLCODE: {}".format(killcode))
    return

@client.event
async def on_member_join(member):
    server = member.server
    fmt = """Welcome {0.mention} to {1.name}. Please tell us your name and when you started so you can join the other channels."""
    await client.send_message(server, fmt.format(member, server))

@client.event
async def on_message(message):
    # await client.send_message(message.channel, "I heard you.")
    #pre message checking to save processing
    #Stop bot checking its own messages
    if message.author == client.user:
        return
    # Whitelist for testing, remove this for main version
    if message.server.name not in ["Omega", "Testing", "Computer Science GC", "asdasd"]:
        return

    # Is the message in the form of a command?
    message_check = re.match('`(.*?)`\\s*(.*)', message.content, re.DOTALL)

    if not message_check:
        # Log message
        # log_to_file("[Server: {} | Channel: {}]: {}".format(message.server, message.channel, message.author, message.content))
        return

    #defines message as `<command> {args1 args2 ... argsN}`<optional_inputs>
    raw_command = re.split(" ", message_check.group(1).strip(" "))
    command = raw_command[0]
    args = raw_command[1:]
    optional_inputs = message_check.group(2).strip(" ")
    # Log command
    log_to_file("""Command received:\nCommand: {}Arguments: {}After: {}""".format(command, args, optional_inputs))
    roles = [x.name.lower() for x in message.author.roles if x.name.lower() != "@everyone"]
    if len(roles) == 0:
         await flash_message(message.channel, "You do not have permission to use commands.", 10)
         return

    if command == 'help':
        success, result = await Commands.help_command(client, message, args, optional_inputs)
        if success:
            await client.send_message(message.channel, result)
        else:
            await flash_message(message.channel, result, 10)
            await client.delete_message(message)
        return

    if command == 'hello':
        success, result = await Commands.hello(client, message, args, optional_inputs)
        if success:
            await client.send_message(message.channel, result)
        else:
            await flash_message(message.channel, result, 10)
            await client.delete_message(message)
        return

    if command == 'kys' and "big-ω" in roles or "amin" in roles:
         if len(args) == 1 and args[0] == killcode:
             await client.logout()
             await client.close()
             return

    if command == 'remind':
        success, result = await Commands.remind(client, message, database, args, optional_inputs)
        if success:
            await flash_message(message.channel, result, 10)
        else:
            await flash_message(message.channel, result, 10)
            await client.delete_message(message)
        return

    if command == 'time':
        await client.send_message(message.channel, "The time is `{}`".format(time.strftime("%d-%m-%Y-%H:%M")))
        return

    if command == 'echo':
        await flash_message(message.channel, "`Echo [{}]:` {}".format(message.author, optional_inputs), 3)
        return

    if command == 'clear' and ("big-ω" in roles or "mods" in roles):
        success, result = await Commands.clear(client, message, args, optional_inputs)
        if success:
            await flash_message(message.channel, result, 5)
        else:
            await flash_message(message.channel, result, 3)
        return

    if command == 'compile':
        success, result = await Commands.compile(client, message, args, optional_inputs)
        if success:
            await client.send_message(message.channel, result)
        else:
            await flash_message(message.channel, result, 20)
            await client.delete_message(message)
        return
    
    if command == "staffContact":
        # Get the course code from the channel name.
        courseCode = message.channel.name[:7]
        
        # Make sure that this command is only being used in a course-specific channel.
        if courseCode[:4].isdigit() and courseCode[4:7] in "icteng":
            result = await Commands.StaffContact(courseCode.upper(), database)
            # If there are no arguments, post to the channel.
            if len(args) < 1:
                await client.send_message(message.channel, result)
            elif len(args) == 1 and args[0] == "private":
                await client.send_message(message.author, result)
        else:
            await client.send_message(message.channel, "This message can only be used in course channels.")
        # If the "private" argument is used, send the information to the user directly. 

    # await flash_message(message.channel, "No command found or you do not have permission.", 5)
client.loop.create_task(reminder_check())
client.run(DISCORD_API_KEY)