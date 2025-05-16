#Loading Log files
filepath= "."
Errorlog= filepath+"/ImportantTxtFiles/Logs/Error.log"
def LogError(Level,Reason):
    with open (Errorlog, "a") as log:
            currenttime= str(time.strftime("%Y-%m-%D %H:%M:%S", time.localtime()))
            log.write(f"{currenttime}    ({Level}) {Reason}\n")
    log.close()
Resourcelog= filepath+"/ImportantTxtFiles/Logs/Resource.log"
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
Generallog= filepath+"/ImportantTxtFiles/Logs/General.log"
LocalFilepath= "/home/server/" #Change this to your local devices filepath
load_dotenv(filepath+"/ImportantTxtFiles/.env")
#load roles (potentially merge this with the settings file)
with open (filepath+"/ImportantTxtFiles/important.csv", "r") as info:
    reader= csv.reader(info)
    for row in reader:
        botrole= row[0]
        Adminrole=row[1]
info.close()



#load settings
with open (filepath+"/ImportantTxtFiles/settings.csv", "r") as settings:
    reader= csv.reader(settings)
    for row in reader:
        LeaderboardDelay= row[0]
        LeaderboardDelay= int(LeaderboardDelay)
        gametype= str(row[1])
        version= str(row[2])
settings.close()


async def loadcogs():
    for filename in os.listdir("./coggers"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"{filename[:-3]} loaded")
async def main():
    async with bot:
        Warningsystemthread= threading.Thread(target=Warningsystem)
        Warningsystemthread.start()
        await loadcogs()
        await bot.start(str(os.getenv("BOT_KEY"))) #rename this to what your bot token variable is called in your .env file
