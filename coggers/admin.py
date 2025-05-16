#Loading Log files
filepath= "."
Errorlog= filepath+"/ImportantTxtFiles/Logs/Error.log"
def LogError(Level,Reason):
    with open (Errorlog, "a") as log:
            currenttime= str(time.strftime("%Y-%m-%D %H:%M:%S", time.localtime()))
            log.write(f"{currenttime}    ({Level}) {Reason}\n")
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



#load settings
with open (filepath+"/ImportantTxtFiles/settings.csv", "r") as settings:
    reader= csv.reader(settings)
    for row in reader:
        LeaderboardDelay= row[0]
        LeaderboardDelay= int(LeaderboardDelay)
        gametype= str(row[1])
        version= str(row[2])
settings.close()


class admin(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    @commands.Cog.listener()
    async def on_ready(self):
         print("admin.py is ready")
    
    #manually shows the usage of the computers resources
    @commands.command()
    async def Usage(self ,ctx):
        person= ctx.author
        personID= person.id
        person= str(person)
        personID= str(personID)
        #Get the load average (1, 5, 15 minutes)
        load_avg = psutil.getloadavg()
        #Get CPU utilization
        cpu_util = psutil.cpu_percent(interval=1)
        #Get memory usage
        memory_info = psutil.virtual_memory()
        await ctx.send(f"Load Average (1, 5, 15 minutes): {load_avg}")
        await ctx.send(f"CPU Utilization: {cpu_util}%")
        await ctx.send(f"Memory Usage: {memory_info.percent}% used ({memory_info.used / (1024**3):.2f} GB / {memory_info.total / (1024**3):.2f} GB)\n<@"+personID+">")

    #Reboots the ENTIRE server/computer (DO NOT TOUCH)
    @commands.command(pass_context=True)
    @commands.has_role(Adminrole)
    async def reboot(self ,ctx):
        global person
        person= ctx.author
        person= str(person)
        print("Bot rebooted by "+ person)
        await ctx.send("rebooting...")
        with open (Generallog, "a") as log:
            currenttime= str(time.strftime("%Y-%m-%D %H:%M:%S", time.localtime()))
            log.write(currenttime+ "   Bot rebooted by "+ person+"\n")
        log.close()
        while True:
            await self.bot.change_presence(status=discord.Status.invisible)
            subprocess.run(["sudo", "reboot"])
            exit()
        pass

    #This will be called if the person running the command does not have the correct role
    @reboot.error
    async def rebootError(self ,ctx ,error):
        global person
        if isinstance(error, commands.CheckFailure):
            person= ctx.author
            personID= person.id
            person= str(person)
            personID= str(personID)
            Level= "Warn"
            Reason= ("Unauthorised Bot reboot attempted by",person)
            await ctx.send("You dont have permissions ("+Adminrole+") to do this <@"+personID+">")
            LogError(Level,Reason)


    @commands.command(pass_context=True)
    @commands.has_role(Adminrole)
    async def update(self, ctx):
        print("Update started...")
        result = subprocess.run(
            ["sudo","git", "pull"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = result.stdout.strip()
        print(output)
        if "Already up to date." in output or "Already up-to-date." in output:
            await ctx.send("Already up to date.")
        else:
            await ctx.send("Bot Updated. If this is a cog update, please `!reload` the cog. If not, reboot the program.")

    @update.error
    async def updateError(self ,ctx ,error):
        global person
        if isinstance(error, commands.CheckFailure):
            person= ctx.author
            personID= person.id
            person= str(person)
            personID= str(personID)
            Level= "Warn"
            Reason= ("Unauthorised Bot update attempted by",person)
            await ctx.send("You dont have permissions ("+Adminrole+") to do this <@"+personID+">")
            LogError(Level,Reason)


async def setup(bot):
      await bot.add_cog(admin(bot))