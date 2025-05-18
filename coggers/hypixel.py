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
import time

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



class hypixel(commands.Cog):
    IG_year = 0
    IG_month = 0
    IG_day = 0
    IG_hour = 0
    IG_minute = 0
    def __init__(self, bot):
        self.bot = bot
        self.first=True
        self.channel = self.bot.get_channel(1372924740993548360)
    @tasks.loop(seconds=4.165)
    async def calenderincrement(self):
        self.IG_minute += 5
        if self.IG_minute >= 60:
            self.IG_minute -= 60
            self.IG_hour += 1
        if self.IG_hour >= 24:
            self.IG_hour = 0
            self.IG_day += 1
        if self.IG_day > 31:
            self.IG_day = 1
            self.IG_month += 1
        if self.IG_month > 12:
            self.IG_month = 1
            self.IG_year += 1
        self.IG_minutetenth = f"{self.IG_minute:02}"
        if self.IG_month== 1:
            self.season= "Early Spring"
        elif self.IG_month== 2:
            self.season= "Spring"
        elif self.IG_month== 3:
            self.season= "Late Spring"
        elif self.IG_month== 4:
            self.season= "Early Summer"
        elif self.IG_month== 5:
            self.season= "Summer"
        elif self.IG_month== 6:
            self.season= "Late Summer"
        elif self.IG_month== 7:
            self.season= "Early Autumn"
        elif self.IG_month== 8:
            self.season= "Autumn"
        elif self.IG_month== 9:
            self.season= "Late Autumn"
        elif self.IG_month== 10:
            self.season= "Early Winter"
        elif self.IG_month== 11:
            self.season= "Winter"
        elif self.IG_month== 12:
            self.season= "Late Winter"
            
        if self.first== True:
            calanderembed=discord.Embed(title="Hypixel Calander", color=0x808080)
            calanderembed.set_thumbnail(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fyt3.ggpht.com%2F-G0UwZhD1hRI%2FAAAAAAAAAAI%2FAAAAAAAAAAA%2FQ5bg4hzv6C0%2Fs900-c-k-no-mo-rj-c0xffffff%2Fphoto.jpg&f=1&nofb=1&ipt=f801051e8936792627a8168f1b1608ee768a1502e30ebdd4407b443eab91cc49")
            calanderembed.add_field(name="Current Hypixel time", value=(f"{self.IG_year}/{self.IG_month}/{self.IG_day}, {int(self.IG_hour)}:{self.IG_minutetenth}"), inline=True)
            calanderembed.add_field(name="Cuurent Season", value=self.season, inline=True)
            calanderembed.add_field(name="", value="", inline=False)
            calanderembed.add_field(name="Current Major Events", value="CurrentEvents", inline=True)
            calanderembed.add_field(name="Major Events soon", value="EventsSoon", inline=True)
            self.calendar_message = await self.channel.send(embed=calanderembed)
            self.first=False
        else:
            calanderembed=discord.Embed(title="Hypixel Calander", color=0x808080)
            calanderembed.set_thumbnail(url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fyt3.ggpht.com%2F-G0UwZhD1hRI%2FAAAAAAAAAAI%2FAAAAAAAAAAA%2FQ5bg4hzv6C0%2Fs900-c-k-no-mo-rj-c0xffffff%2Fphoto.jpg&f=1&nofb=1&ipt=f801051e8936792627a8168f1b1608ee768a1502e30ebdd4407b443eab91cc49")
            calanderembed.add_field(name="Current Hypixel time", value=(f"{self.IG_year}/{self.IG_month}/{self.IG_day}, {int(self.IG_hour)}:{self.IG_minutetenth}"), inline=True)
            calanderembed.add_field(name="Cuurent Season", value="season", inline=True)
            calanderembed.add_field(name="", value="", inline=False)
            calanderembed.add_field(name="Current Major Events", value="CurrentEvents", inline=True)
            calanderembed.add_field(name="Major Events soon", value="EventsSoon", inline=True)
            await self.calendar_message.edit(embed=calanderembed)

    async def calenderinit(self):
        time.sleep(0.1)
        while True:
            utc_now = datetime.now(timezone.utc)
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
            self.IG_year = IG_year+1
            self.IG_month = IG_month + 1   # +1 for human-readable months
            self.IG_day = IG_day + 1       # +1 for human-readable days
            self.IG_hour = int(IG_hour)
            self.IG_minute = int(IG_minute)
            self.IG_minutetenth = f"{self.IG_minute:02}"
            if int(round(self.IG_minute)) % 5 == 0:
                await self.calenderincrement.start()
                break

    @commands.Cog.listener()
    async def on_ready(self):
        print("hypixel.py is ready")
        self.channel = self.bot.get_channel(1372924740993548360)
        await self.channel.purge()
        await self.calenderinit()
        
    

async def setup(bot):
      await bot.add_cog(hypixel(bot))