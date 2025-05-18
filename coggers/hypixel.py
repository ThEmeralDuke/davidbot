filepath= "."
#loading libraries
import os
import os.path
from dotenv import *
import discord
from discord import *
from discord.ext import commands, tasks
from discord.utils import *
from datetime import datetime, timezone
import csv
import psutil
import random
import threading
import subprocess
import keyboard
import json
import asyncio

#stuff
botrole= []
Adminrole= []
person= ""
Generallog= filepath+"/ImportantTxtFiles/Logs/General.log"
LocalFilepath= "/home/server/" #Change this to your local devices filepath
#load roles (potentially merge this with the settings file)
with open (filepath+"/ImportantTxtFiles/important.csv", "r") as info:
    reader= csv.reader(info)
    for row in reader:
        botrole= row[0]
        Adminrole=row[1]
info.close()
utc_now = datetime.now(timezone.utc)
skyblockstart = datetime.strptime("2019-06-11 17:55:00", "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)

IG_year = 0
IG_month = 0
IG_day = 0
IG_hour = 0
IG_minute = 0
def initialise_ig_time():
    global IG_year
    global IG_month
    global IG_day
    global IG_hour
    global IG_minute
    global utc_now
    skyblockstart = datetime.strptime("2019-06-11 17:55:00", "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    #IRL time
    secondssincestart = (utc_now - skyblockstart).total_seconds()
    minutessincestart = int(secondssincestart// 60)
    #IG time
    # Skyblock time constants (in real minutes)
    MINUTES_PER_IG_MINUTE = 0.01388      # 0.833 seconds
    MINUTES_PER_IG_HOUR = 0.8333         # 50 seconds
    MINUTES_PER_IG_DAY = 20
    MINUTES_PER_IG_MONTH = 620
    MINUTES_PER_IG_YEAR = 7440

    # Compute each unit from the largest to the smallest
    IG_year, remainder = divmod(minutessincestart, MINUTES_PER_IG_YEAR)
    IG_month, remainder = divmod(remainder, MINUTES_PER_IG_MONTH)
    IG_day, remainder = divmod(remainder, MINUTES_PER_IG_DAY)
    IG_hour, remainder = divmod(remainder, MINUTES_PER_IG_HOUR)
    IG_minute, _ = divmod(remainder, MINUTES_PER_IG_MINUTE)

    # Convert to integers for display
    IG_year = int(IG_year)+1
    IG_month = int(IG_month) + 1   # +1 for human-readable months
    IG_day = int(IG_day) + 1       # +1 for human-readable days
    IG_hour = int(IG_hour)
    IG_minute = int(IG_minute)

    print(f"Year: {IG_year}, Month: {IG_year}, Day: {IG_year}, Hour: {IG_year}, Minute: {IG_year}")
class hypixel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.calenderincrement.start()
    @commands.Cog.listener()
    async def on_ready(self,bot):
        print("hypixel.py is ready")

    @tasks.loop(seconds=4.165)
    async def calenderincrement(self,ctx):
        global IG_year
        global IG_month
        global IG_day
        global IG_hour
        global IG_minute
        IG_minute += 5
        if IG_minute >= 60:
            IG_minute -= 60
            IG_hour += 1
        if IG_hour >= 24:
            IG_hour = 0
            IG_day += 1
        if IG_day > 31:
            IG_day = 1
            IG_month += 1
        if IG_month > 12:
            IG_month = 1
            IG_year += 1
        print(f"Year: {IG_year}, Month: {IG_year}, Day: {IG_year}, Hour: {IG_year}, Minute: {IG_year}")
        #embed=discord.Embed(title="Hypixel Calander", color=0x808080)
        #embed.set_thumbnail(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fyt3.ggpht.com%2F-G0UwZhD1hRI%2FAAAAAAAAAAI%2FAAAAAAAAAAA%2FQ5bg4hzv6C0%2Fs900-c-k-no-mo-rj-c0xffffff%2Fphoto.jpg&f=1&nofb=1&ipt=f801051e8936792627a8168f1b1608ee768a1502e30ebdd4407b443eab91cc49")
        #embed.add_field(name="Current Hypixel time", value="(date+time+ToD)", inline=True)
        #embed.add_field(name="Cuurent Season", value="season", inline=True)
        #embed.add_field(name="", value="", inline=False)
        #embed.add_field(name="Current Major Events", value="CurrentEvents", inline=True)
        #embed.add_field(name="Major Events soon", value="EventsSoon", inline=True)
        #await calenderchannel.send(embed=embed)
initialise_ig_time()
async def setup(bot):
      await bot.add_cog(hypixel(bot))