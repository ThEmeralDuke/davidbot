filepath= "."
#loading libraries
import discord
from discord import *
from discord.ext import commands, tasks
from discord.utils import *
from datetime import datetime, timezone
import csv
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



class hypixel(commands.Cog):
    def __init__(self, bot):
        # variables
        self.bot = bot
        self.current_events=[]
        # Placeholders
        self.channel = None
        self.loop_started= False
        self.calendar_message = None
        self.first = True
        self.season = 0  
        self.IG_year = 0
        self.IG_month = 0
        self.IG_day = 0
        self.IG_hour = 0
        self.IG_minute = 0
        self.IG_minutetenth = "00"
        self.Jacob_event= False
        self.Dark_Auction= False
        self.Hop_Hunt= False
        self.Zoo = False
        self.Cult = False
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("hypixel.py is ready")
        self.channel = self.bot.get_channel(1372924740993548360)  # Replace with actual ID
        await self.channel.purge()
        await self.update_calendar()
    # Wait until in-game minute is a multiple of 10
        i=True
        while i==True:
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
            IG_minute = int(round(IG_minute))


            if IG_minute % 1 == 0:
                print(f"Aligned to IGT minute {IG_minute}. Starting loop.")
                i=False
                self.loop_started= True
                self.update_calendar_loop.start()
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
        self.IG_minute = int(round(self.IG_minute))
        if self.IG_minute % 10 == 0:
            pass
        else:
            self.IG_minute= int((IG_minute // 10) * 10)
            if self.IG_minute == 60:
                self.IG_minute = 0
                self.IG_hour = self.IG_hour + 1
        self.IG_monthtenth = f"{self.IG_month:02}"
        self.IG_hourtenth = f"{self.IG_hour:02}"
        self.IG_minutetenth = f"{self.IG_minute:02}"
        self.seasons=["Early Spring","Spring","Late Spring","Early Summer","Summer","Late Summer","Early Autumn","Autumn","Late Autumn","Early Winter","Winter","Late Winter"]
        self.season= self.seasons[int(IG_month)]
    def get_events(self):
        self.Current_IRL_Minute= int((datetime.now()).strftime("%M"))
        if self.Current_IRL_Minute== 55 and self.Dark_Auction== False:
            self.Dark_Auction = True
            self.current_events.append("Dark Auction")
        elif self.Dark_Auction == True and self.Current_IRL_Minute != 55:
            self.Dark_Auction = False
            self.current_events.remove("Dark Auction")
        if 15<= self.Current_IRL_Minute <=34 and self.Jacob_event==False:
            self.Jacob_event = True
            self.current_events.append("Jacob's Farming")
        elif self.Jacob_event == True and self.Current_IRL_Minute >= 35:
            self.Jacob_event = False
            self.current_events.remove("Jacob's Farming")
        if "Spring" in self.seasons[int(self.IG_month-1)]  and self.Hop_Hunt==False:
            self.Hop_Hunt = True
            self.current_events.append("Hoppity's Hunt")
        elif self.Hop_Hunt == True and "Spring" not in self.seasons[int(self.IG_month-1)]:
            self.Jacob_event = False
            self.current_events.remove("Hoppity's Hunt")
        if "Early Summer" in self.seasons[int(self.IG_month-1)] and "Early Winter" in self.seasons[int(self.IG_month-1)] and 1 <= self.IG_day <= 3 and self.Zoo==False:
            self.Zoo = True
            print("Zoo TRUE")
            self.current_events.append("Traveling Zoo")
        elif self.Zoo == True and self.IG_day >= 3:
            self.Zoo = False
            self.current_events.remove("Traveling Zoo")
        if self.Cult == False:
            self.conjoinedtime= int(str(self.IG_hour)+str(self.IG_minutetenth))
            print(self.conjoinedtime)
            #if self.IG_day in (7,14,21,28) and self.conjoinedtime<=:
             #   
              #  self.Cult= True
               # self.current_events.append("Star Cult Meeting")

        self.current_event_list= "\n".join(self.current_events)

    async def update_calendar(self):
        if self.loop_started== True:
            self.get_ig_time()
            self.get_events()
            calanderembed = discord.Embed(title="Hypixel Calander", color=0x808080)
            calanderembed.set_thumbnail(url="attachment://ImportantTxtFiles/Hypixel/HypixelLogo.png")
            calanderembed.add_field(name="Current Hypixel time", value=(f"{self.IG_day}/{self.IG_monthtenth}/{self.IG_year}, {self.IG_hourtenth}:{self.IG_minutetenth}"), inline=True)
            calanderembed.add_field(name="Cuurent Season", value=self.season, inline=True)
            calanderembed.add_field(name="", value="", inline=False)
            calanderembed.add_field(name="Current Major Events", value=self.current_event_list, inline=True)


            if self.first:
                self.calendar_message = await self.channel.send(embed=calanderembed)
                self.first = False
            else:
                await self.calendar_message.edit(embed=calanderembed)

    @tasks.loop(seconds=0.75)
    async def update_calendar_loop(self):
        await self.update_calendar()


        
    

async def setup(bot):
      await bot.add_cog(hypixel(bot))