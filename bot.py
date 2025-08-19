#Loading Log files
filepath= "."
Errorlog= filepath+"/ImportantTxtfiles/Logs/Error.log"
def LogError(Level,Reason):
    with open (Errorlog, "a") as log:
            currenttime= str(time.strftime("%Y-%m-%D %H:%M:%S", time.localtime()))
            log.write(f"{currenttime}    ({Level}) {Reason}\n")
    log.close()
Resourcelog= filepath+"/ImportantTxtfiles/Logs/Resource.log"
def LogResource(Level,Reason,Percent):
    if Level=="Critical":
        descriptor= "very high"
    elif Level=="Serious":
        descriptor= "high"
    else:
        descriptor= "getting high"
    currenttime= str(time.strftime("%H:%M:%S", time.localtime()))
    print(f"{currenttime}    ({Level}) {Reason} usage {descriptor} ({Percent}%)")
    with open (Resourcelog, "a") as log:
        currenttime= str(time.strftime("%Y-%m-%D %H:%M:%S", time.localtime()))
        log.write(f"{currenttime}    ({Level}) {Reason} at {Percent}%\n")

    log.close()

#loading libraries
import os
import os.path
from dotenv import *
import discord
from discord import *
from discord.ext import commands
from discord.utils import *
import time
import csv
import random
import threading
import subprocess
import psutil
import keyboard
import json
import asyncio

#stuff
botrole= []
Adminrole= []
person= ""
Generallog= filepath+"/ImportantTxtfiles/Logs/General.log"
LocalFilepath= "/home/server/" #Change this to your local devices filepath
load_dotenv(filepath+"/ImportantTxtfiles/.env")
#load roles (potentially merge this with the settings file)
with open (filepath+"/ImportantTxtfiles/important.csv", "r") as info:
    reader= csv.reader(info)
    for row in reader:
        botrole= row[0]
        Adminrole=row[1]
info.close()



#load settings
with open (filepath+"/ImportantTxtfiles/settings.csv", "r") as settings:
    reader= csv.reader(settings)
    for row in reader:
        LeaderboardDelay= row[0]
        LeaderboardDelay= int(LeaderboardDelay)
        gametype= str(row[1])
        version= str(row[2])
settings.close()

#SystemChannelID= 1240997501750743221 #This should be the test channel for your bot to see if it starts (delete if unnessecary)
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), activity = discord.Activity(type=discord.ActivityType.listening, name="!Commands"))
#Wanrs the user if the ram or cpu usage is too high
def Warningsystem():
    while True:
        memory_info = psutil.virtual_memory()
        rampercent= float(f"{memory_info.percent}")
        cpu_util = psutil.cpu_percent(interval=1)
        if rampercent >=95:
            LogResource("Critical","RAM",rampercent)
        elif rampercent >=85:
            LogResource("Serious","RAM",rampercent)
        elif rampercent >=75:
            LogResource("Warning","RAM",rampercent)
        if cpu_util >=95:
            LogResource("Critical","CPU",cpu_util)
        elif cpu_util >=85:
            LogResource("Serious","CPU",cpu_util)
        elif cpu_util >=75:
            LogResource("Warning","CPU",cpu_util)
        time.sleep(20)





#Commands of what the bot can do
@bot.command()
async def Commands(ctx):
    person= ctx.author
    personID= person.id
    person= str(person)
    personID= str(personID)
    await ctx.send("List of commands: (Case sensitive)\n. !Usage\n2. !reboot (admin protected)\n3. !MCrestart\n4. !MCbackup (admin protected)"
    "\n5. !startRR\n6. !RRleaderboard\n7. !QuitRR\n8. !reload help\n\n<@"+personID+">")

Coglist= []
async def loadcogs():
    global Coglist
    Coglist= []
    for filename in os.listdir("./coggers"):
        if filename.endswith(".py"):
            await bot.load_extension(f"coggers.{filename[:-3]}")
            print(f"{filename[:-3]} loaded")
            Coglist.append(filename[:-3])


@bot.command()
@commands.has_role(Adminrole)
async def reload(ctx,arg=None):
    # Reloads the file, thus updating the Cog class.
    if arg is None:
        await ctx.send("Please provide an argument, If you are confused use !reload help")
    arg= arg.lower()
    if arg== "help":
        await ctx.send("Reload Help.\n\n!reload list - provides a list of cogs available to be reloaded\n\n!reload all - Reloads all cogs (including new cogs)")
    elif arg=="list":
        await ctx.send("Cogs able to be reloaded:\n"+"\n".join(Coglist))
    elif arg== "all":
        for filename in os.listdir("./coggers"):
            if filename.endswith(".py") and filename[:-3] in Coglist:
                await bot.reload_extension(f"coggers.{filename[:-3]}")
                print(f"{filename[:-3]} reloaded")
            else:
                await bot.load_extension(f"coggers.{filename[:-3]}")
                print(f"{filename[:-3]} loaded")
    elif arg in Coglist:
        await bot.reload_extension(f"coggers.{arg}")
        print(f"{arg} reloaded")
    else: 
        await ctx.send("Cog not found. Use !reload list")

@bot.command()
@commands.has_role(Adminrole)
async def disable(ctx,arg=None):
    if arg is None:
        await ctx.send("Please provide an argument, To see all possible options use !disable list")
    arg= arg.lower()
    if arg=="list":
        await ctx.send("Cogs able to be reloaded:\n"+"\n".join(Coglist))
    if arg in Coglist:
        #await bot.reload_extension(f"coggers.{arg}") replace with the deload script
        print(f"{arg} Disabled for serverID:")#after for say the server ID    



async def main():
    async with bot:
        Warningsystemthread= threading.Thread(target=Warningsystem)
        Warningsystemthread.start()
        await loadcogs()
        await bot.start(str(os.getenv("BOT_KEY"))) #rename this to what your bot token variable is called in your .env file
        
asyncio.run(main())
