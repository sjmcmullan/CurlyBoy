import discord
import requests
import re
import json
import asyncio
import sqlite3
import time
import lang
import helper

HACKERRANK_URL = 'http://api.hackerrank.com/checker/submission.json'
HACKERRANK_API_KEY = 'hackerrank|3491785-2301|18ff1e697a4f9435ceba9e9c87f01ad8d1bfc854'
HACKERRANK_LANGUAGE_CODES = {
 'fsharp':  33, 'javascript': 20, 'whitespace': 41, 'python2':     5, 'lolcode':     38,
 'mysql':   10, 'fortran':    54, 'tcl':        40, 'oracle':     11, 'pascal':      25,
 'haskell': 12, 'cobol':      36, 'octave':     46, 'csharp':      9, 'go':          21,
 'php':      7, 'ruby':        8, 'java8':      43, 'bash':       14, 'visualbasic': 37,
 'groovy':  31, 'c':           1, 'erlang':     16, 'java':        3, 'd':           22,
 'scala':   15, 'tsql':       42, 'ocaml':      23, 'perl':        6, 'lua':         18,
 'xquery':  48, 'r':          24, 'swift':      51, 'sbcl':       26, 'smalltalk':   39,
 'racket':  49, 'cpp':         2, 'db2':        44, 'objectivec': 32, 'clojure':     13,
 'python':  30, 'python3':    30, 'rust':       50
}
#######################################################################################################
#Command:     help
#Arguments:   <command>
#Inputs:      COMMAND=N/A
#Description: Gives a description on the Commands.
#######################################################################################################
async def help_command(client, message, args, optional_inputs):
    if len(args) == 1 and helper.command_discription[args[0]]:
        return True, "```\n"+helper.command_discription[args[0]]+"```"
    else:
        return True, "```"+"\n".join([x for x in helper.command_discription.keys() if x not in ["kys"]])+"```"
#######################################################################################################
# END of hello
#######################################################################################################



#######################################################################################################
#Command:     hello
#Arguments:   <language>
#Inputs:      LANGUAGE=N/A
#Description: Gives an example hello world in given language
#######################################################################################################
async def hello(client, message, args, optional_inputs):
    if len(args) == 1 and lang.lang_dict[args[0]]:
        return True, "```"+args[0]+"\n"+lang.lang_dict[args[0]]+"```"
    else:
        return False, "Invalid language or command structure. `hello <language_shorthand>` i.e.\n`hello python`"
#######################################################################################################
# END of hello
#######################################################################################################



#######################################################################################################
#Command:     remind
#Arguments:   date <YYYY-MM-DD-HH:mm>, in <seconds from current time>
#Inputs:      DATE=<content of reminder>  IN=<content of reminder>
#Description: Reminds (given a time/date) everything typed after the command.
#######################################################################################################
async def remind(client, message, database, args, optional_inputs):
    public = 1
    if len(args) == 0:
        return False, "Please enter argument: date|in."
    if len(args) == 1:
        return False, "Please enter 2 arguments. One for type date|in and other for input:\n `DATE=YYYY-MM-DD-HH:mm   IN=<seconds from current time>`"
    if len(args) == 3 and args[2] == 'private':
        public = 0
    if args[0] == 'date':
        try:
            time_end = time.strptime(args[1], "%d-%m-%Y-%H:%M")
        except:
            return False, "Invalid time given. please use DD-MM-YYYY-HH:mm"
        time_started = time.localtime()
        if time_end > time_started:
            c = database.cursor()
            c.execute('''
            INSERT INTO reminders(time_started, time_end, creator, channel, public, description)
            VALUES (?,?,?,?,?,?)
            ''', (time.strftime("%d-%m-%Y-%H:%M", time_started), time.strftime("%d-%m-%Y-%H:%M", time_end), message.author.id, message.channel.id, public, optional_inputs))
            database.commit()
            if public == 1:
                return True, "Reminder added. Will remind this channel at "+args[1]+"."
            else:
                return True, "Reminder added. Will remind "+message.author.mention+" at "+args[1]+"."
        else:
            return False, "Time is not greater than current time."

    elif args[0] == 'in':
        #not implemented
        return False, "Not implemented."
    return False, "Unknown Error."
#######################################################################################################
# END of remind
#######################################################################################################


#######################################################################################################
#Command:     clear
#Arguments:   "", limit, until
#Inputs:      LIMIT=1-100   UNTIL=<Keyword or message>
#Description: Deletes messages from channel it was entered in.
#######################################################################################################
async def clear(client, message, args, optional_inputs):
    if len(args) == 0:
        logs = [x async for x in client.logs_from(message.channel, limit=2)]
        await client.delete_messages(logs)
        return True, "Deleted previous message. :)"
    elif len(args) == 1:
        clear_type = args[0]
        if clear_type == "limit":
            try:
                limit_to = int(optional_inputs)
                logs = [x async for x in client.logs_from(message.channel, limit=int(limit_to)+1)]
                await client.delete_messages(logs)
                return True, "Deleted "+str(len(logs))+" message(s). :)"
            except:
                return False, "Could not delete. \n**Note:**Must be integer & argument must be less than 100."
        elif clear_type == "until":
            if len(optional_inputs) == 0:
                return False, "Please insert the beginning of the message you which to delete until"
            logs = [x async for x in client.logs_from(message.channel, limit=100)]
            content = [x.content for x in logs]
            for i in range(len(content)):
                if content[i].startswith(optional_inputs):
                    if i <= 1:
                        await client.delete_message(message)
                        return False, "No messages to delete."
                    await client.delete_messages(logs[:i])
                    return True, "Deleted "+str(i)+" message(s). :)"
            return False, "Could not find message given."
        else:
            return False, "Not enough arguments.\n Command structure: `clear <\"\"|\"until\"|\"limit\">` <\"\"|<Keyword or message>|1-100>"
    return False, "Unknown Error."
#######################################################################################################
# END of clear
#######################################################################################################



#######################################################################################################
#Command:     compile
#Arguments:   languages, block <language>, file <language>
#Inputs:      LANGUAGES=N/A,   BLOCK=```<source>``` <testcases>, FILE=<FILE of source> <testcases>
#Description: Using hackerranks api to compile straight from discord and reply the outcome.
#######################################################################################################
async def compile(client, message, args, optional_inputs):
    if len(args) == 1 and args[0] == "languages":
        languages = sorted(HACKERRANK_LANGUAGE_CODES.keys())
        return True, "Available languages: \n ```"+", \n".join(languages)+"```"

    if len(args) < 2:
        return False, "Not enough arguments.\n Command structure: `compile <\"file\"|\"block\"> <language>` ```<source|\"attached_source\">``` <optional_inputs>"

    if len(args) > 2:
        return False, "Too many arguments.\n Command structure: `compile <\"file\"|\"block\"> <language>` ```<source|\"attached_source\">``` <optional_inputs>"


    if args[0] == 'block':
        block_check = re.match("```(.*?)\\W(.*?)```(.*)", optional_inputs, re.DOTALL)
        if not block_check:
            return False, "No block detected in message. Are you sure you attached the code? :)"
        markup_language = block_check.group(1)
        block = block_check.group(2)
        optional_inputs = block_check.group(3)

    inputs = [''.join(x) for x in re.findall("""\\s*["]([^"]*?)["]\\s*|\\s*\\b\\s*(.+?)\\s*\\b\\s*""", optional_inputs)]

    if not inputs:
        # Ensure that at least 1 test case is run if no input is provided
        inputs = [""]


    if args[0] == 'file':
        if not len(message.attachments):
            return False, "No file detected in message. Are you sure you attached the code? :)"
        attachment_url = message.attachments[0]['url']
        returned_file = requests.get(attachment_url)
        source = returned_file.text
    elif args[0] == 'block':
        source = block
    else:
        return False, "Please put in your source as a file or block.\n Command structure: `compile <\"file\"|\"block\"> <language>` ```<source|\"attached_source\">``` <optional_inputs>"

    #Checks that the language provided is one that hackerrank can compile
    lang = args[1]
    if not lang in HACKERRANK_LANGUAGE_CODES.keys():
        return False, "Invalid language \"{}\". Check supported languages with the `compile languages` command.".format(lang)

    params = {'api_key': HACKERRANK_API_KEY,
            'source': source,
            'lang': HACKERRANK_LANGUAGE_CODES[lang],
            'testcases': json.dumps(inputs),
            'format': "json"}
    try:
        response = requests.post(HACKERRANK_URL, data=params)
    except:
        return False, "Error: ```\nBad Request.```"
    if response.status_code != 200:
        return False, "Error: ```\nRequest status code is "+str(response.status_code)+".```"
    response = response.json()['result']

    if response["stderr"] and response["stderr"][0]:
        return False, "Error: ```diff\n- {}```".format("\n".join(response["stderr"]).replace("\\n","\n"))

    if response["message"] and not response["message"][0] == "Success":
        return False, "Error: ```{}```".format(response["message"][0]).replace("\\n","\n")

    if not response["message"]:
        if response["compilemessage"]:
            return False, "Compile error: ```diff\n- {}```".format(response["compilemessage"]).replace("\\n","\n")
        else:
            return False, "Unknown error."

    if response["stdout"]:
        return True, "\n".join(["```\n{}\n```".format(x) for x in response["stdout"]])
    else:
        return True, "No output."\
#######################################################################################################
# END of compile
#######################################################################################################
