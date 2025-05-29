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
        self.channel = None
        self.calendar_message = None
        self.first = True
        self.season = "Spring"  # Placeholder; you can add logic to set this based on date
        self.IG_year = 0
        self.IG_month = 0
        self.IG_day = 0
        self.IG_hour = 0
        self.IG_minute = 0
        self.IG_minutetenth = "00"

    @commands.Cog.listener()
    async def on_ready(self):
        print("hypixel.py is ready")
        self.channel = self.bot.get_channel(1372924740993548360)  # Replace with actual ID
        await self.channel.purge()
        await self.update_calendar()
        self.update_calendar_loop.start()
    # Wait until in-game minute is a multiple of 5
        while True:
            utc_now = datetime.now(timezone.utc)
            skyblock_start = datetime.strptime("2019-06-11 17:55:00", "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
            seconds_since_start = (utc_now - skyblock_start).total_seconds()
            minutes_since_start = int(seconds_since_start // 60)

            # Skyblock time constants
            MINUTES_PER_IG_MINUTE = 0.01388
            MINUTES_PER_IG_HOUR = 0.8333
            MINUTES_PER_IG_DAY = 20
            MINUTES_PER_IG_MONTH = 620
            MINUTES_PER_IG_YEAR = 7440

            _, remainder = divmod(minutes_since_start, MINUTES_PER_IG_YEAR)
            _, remainder = divmod(remainder, MINUTES_PER_IG_MONTH)
            _, remainder = divmod(remainder, MINUTES_PER_IG_DAY)
            _, remainder = divmod(remainder, MINUTES_PER_IG_HOUR)
            IG_minute, _ = divmod(remainder, MINUTES_PER_IG_MINUTE)
            IG_minute = int(IG_minute)

            if IG_minute % 5 == 0:
                print(f"Aligned to IGT minute {IG_minute}. Starting loop.")
                self.calenderincrement.start()
                break
            else:
                await asyncio.sleep(1)  # Wait a second and try again
    def get_ig_time(self):
        utc_now = datetime.now(timezone.utc)
        skyblock_start = datetime.strptime("2019-06-11 17:55:00", "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        seconds_since_start = (utc_now - skyblock_start).total_seconds()
        total_real_minutes = seconds_since_start / 60

        MINUTES_PER_IG_MINUTE = 0.01388
        MINUTES_PER_IG_HOUR = 0.8333
        MINUTES_PER_IG_DAY = 20
        MINUTES_PER_IG_MONTH = 620
        MINUTES_PER_IG_YEAR = 7440

        IG_year, remainder = divmod(total_real_minutes, MINUTES_PER_IG_YEAR)
        IG_month, remainder = divmod(remainder, MINUTES_PER_IG_MONTH)
        IG_day, remainder = divmod(remainder, MINUTES_PER_IG_DAY)
        IG_hour, remainder = divmod(remainder, MINUTES_PER_IG_HOUR)
        IG_minute, _ = divmod(remainder, MINUTES_PER_IG_MINUTE)

        self.IG_year = int(IG_year) + 1
        self.IG_month = int(IG_month) + 1
        self.IG_day = int(IG_day) + 1
        self.IG_hour = int(IG_hour)
        self.IG_minute = int(IG_minute)
        self.IG_monthtenth = f"{self.IG_month:02}"
        self.IG_hourtenth = f"{self.IG_hour:02}"
        self.IG_minutetenth = f"{self.IG_minute:02}"
        seasons=["Early Spring","Spring","Late Spring","Early Summer","Summer","Late Summer","Early Autumn","Autumn","Late Autumn","Early Winter","Winter","Late Winter"]
        self.season= seasons[int(IG_month)]
    async def update_calendar(self):
        self.get_ig_time()
        calanderembed = discord.Embed(title="Hypixel Calander", color=0x808080)
        calanderembed.set_thumbnail(url="attachment://ImportantTxtFiles/HypixelLogo.png")
        calanderembed.add_field(name="Current Hypixel time", value=(f"{self.IG_year}/{self.IG_monthtenth}/{self.IG_day}, {int(self.IG_hourtenth)}:{self.IG_minutetenth}"), inline=True)
        calanderembed.add_field(name="Cuurent Season", value=self.season, inline=True)
        calanderembed.add_field(name="", value="", inline=False)
        calanderembed.add_field(name="Current Major Events", value="CurrentEvents", inline=True)
        calanderembed.add_field(name="Major Events soon", value="EventsSoon", inline=True)

        if self.first:
            self.calendar_message = await self.channel.send(embed=calanderembed)
            self.first = False
        else:
            await self.calendar_message.edit(embed=calanderembed)

    @tasks.loop(seconds=4.165)
    async def update_calendar_loop(self):
        await self.update_calendar()


        
    

async def setup(bot):
      await bot.add_cog(hypixel(bot))