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
    
    def __init__(self, bot):
        self.bot = bot
        self.first=True
        self.channel = self.bot.get_channel(1372924740993548360)
        self.calenderincrement = tasks.loop(seconds=4.165)(self.update_calendar)
        self.IG_year = 0
        self.IG_month = 0
        self.IG_day = 0
        self.IG_hour = 0
        self.IG_minute = 0
        self.season= None
    i=True
    async def calenderinit(self):
        while True:
            utc_now = datetime.now(timezone.utc)
            skyblockstart = datetime.strptime("2019-06-11 17:55:00", "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
            secondssincestart = (utc_now - skyblockstart).total_seconds()
            minutessincestart = int(secondssincestart // 60)

            # Skyblock time constants
            MINUTES_PER_IG_MINUTE = 0.01388
            MINUTES_PER_IG_HOUR = 0.8333
            MINUTES_PER_IG_DAY = 20
            MINUTES_PER_IG_MONTH = 620
            MINUTES_PER_IG_YEAR = 7440

            IG_year, remainder = divmod(minutessincestart, MINUTES_PER_IG_YEAR)
            IG_month, remainder = divmod(remainder, MINUTES_PER_IG_MONTH)
            IG_day, remainder = divmod(remainder, MINUTES_PER_IG_DAY)
            IG_hour, remainder = divmod(remainder, MINUTES_PER_IG_HOUR)
            IG_minute, _ = divmod(remainder, MINUTES_PER_IG_MINUTE)

            self.IG_year = IG_year + 1
            self.IG_month = IG_month + 1
            self.IG_day = IG_day + 1
            self.IG_hour = int(IG_hour)
            self.IG_minute = int(IG_minute)
            self.IG_minutetenth = f"{self.IG_minute:02}"
            if self.IG_minute % 5 == 0:
                print(f"Initial IG time: {self.IG_year}-{self.IG_month}-{self.IG_day} {self.IG_hour}:{self.IG_minutetenth}")
                if not self.calenderincrement.is_running():
                    self.calenderincrement.start()
                break


    async def update_calendar(self):
        # Recalculate current IG time
        utc_now = datetime.now(timezone.utc)
        skyblockstart = datetime.strptime("2019-06-11 17:55:00", "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        secondssincestart = (utc_now - skyblockstart).total_seconds()
        minutessincestart = int(secondssincestart // 60)

        MINUTES_PER_IG_MINUTE = 0.01388
        MINUTES_PER_IG_HOUR = 0.8333
        MINUTES_PER_IG_DAY = 20
        MINUTES_PER_IG_MONTH = 620
        MINUTES_PER_IG_YEAR = 7440

        IG_year, remainder = divmod(minutessincestart, MINUTES_PER_IG_YEAR)
        IG_month, remainder = divmod(remainder, MINUTES_PER_IG_MONTH)
        IG_day, remainder = divmod(remainder, MINUTES_PER_IG_DAY)
        IG_hour, remainder = divmod(remainder, MINUTES_PER_IG_HOUR)
        IG_minute, _ = divmod(remainder, MINUTES_PER_IG_MINUTE)

        self.IG_year = IG_year + 1
        self.IG_month = IG_month + 1
        self.IG_day = IG_day + 1
        self.IG_hour = int(IG_hour)
        self.IG_minute = int(IG_minute)
        self.IG_minutetenth = f"{self.IG_minute:02}"
        if self.first== True:
            calanderembed=discord.Embed(title="Hypixel Calander", color=0x808080)
            calanderembed.set_thumbnail(url="attachment://ImportantTxtFiles/HypixelLogo.png")
            calanderembed.add_field(name="Current Hypixel time", value=(f"{self.IG_year}/{self.IG_month}/{self.IG_day}, {int(self.IG_hour)}:{self.IG_minutetenth}"), inline=True)
            calanderembed.add_field(name="Cuurent Season", value=self.season, inline=True)
            calanderembed.add_field(name="", value="", inline=False)
            calanderembed.add_field(name="Current Major Events", value="CurrentEvents", inline=True)
            calanderembed.add_field(name="Major Events soon", value="EventsSoon", inline=True)
            self.calendar_message = await self.channel.send(embed=calanderembed)
            self.first=False
        else:
            calanderembed=discord.Embed(title="Hypixel Calander", color=0x808080)
            calanderembed.set_thumbnail(url="attachment://ImportantTxtFiles/HypixelLogo.png")
            calanderembed.add_field(name="Current Hypixel time", value=(f"{self.IG_year}/{self.IG_month}/{self.IG_day}, {int(self.IG_hour)}:{self.IG_minutetenth}"), inline=True)
            calanderembed.add_field(name="Cuurent Season", value=self.season, inline=True)
            calanderembed.add_field(name="", value="", inline=False)
            calanderembed.add_field(name="Current Major Events", value="CurrentEvents", inline=True)
            calanderembed.add_field(name="Major Events soon", value="EventsSoon", inline=True)
            await self.calendar_message.edit(embed=calanderembed)
    @commands.Cog.listener()
    async def on_ready(self):
        print("hypixel.py is ready")
        self.channel = self.bot.get_channel(1372924740993548360)
        await self.channel.purge()
        asyncio.create_task(self.calenderinit())

        
    

async def setup(bot):
      await bot.add_cog(hypixel(bot))