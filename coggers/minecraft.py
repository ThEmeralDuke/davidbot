#Loading Log files
filepath= "."
Errorlog= filepath+"/ImportantTxtfiles/Logs/Error.log"
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
import random
import subprocess
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

##Minecraft settings##

Minecraftserverfilepath="/home/server/Minecraft" #Change this to the filepath of your minecraft server
#Minecraftbackupfilepath="/opt/backups/minecraft/"+gametype+"/"+version+"/" #Change this to the filepath of your minecraft server backups
class minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    @commands.Cog.listener()
    async def on_ready(self):
         print("minecraft.py is ready")
    #This remotely restarts the minecraft server
    @commands.command(pass_context=True)
    @commands.has_role(Adminrole)
    async def MCrestart(self ,ctx):
        global person
        person= ctx.author
        person= str(person)
        print("Minecraft rebooted by "+ person)
        await ctx.send("Restarting Minecraft...")
        with open (Generallog, "a") as log:
            currenttime= str(time.strftime("%Y-%m-%D %H:%M:%S", time.localtime()))
            log.write(currenttime+ "   Minecraft restarted by "+ person+"\n")
        log.close
        try:
            try:
                #sends the command to the tmux session
                subprocess.run(["sudo","-u","server","tmux", "send-keys", "-t", "Minecraft", "ENTER"])
                subprocess.run(["sudo","-u","server","tmux", "send-keys", "-t", "Minecraft", "stop", "ENTER"])
                #subprocess.run(["sudo","-u","server","tmux", "send-keys", "-t", "Minecraft", "/stop", "ENTER"])
                await ctx.send("Minecraft shut down correctly and rebooting")
                sleepyboi= 10
            except:
                sleepyboi= 0
            time.sleep(sleepyboi) #Just give it more time to close
            subprocess.run(["sudo", "-u", "server", "/bin/bash", "/home/server/sh/mcstart.sh"])
            time.sleep(35) #Give it time to start
            subprocess.run(['sudo -u server ssh -i ~/.ssh/ssh* ubuntu@132.145.78.199 "sudo reboot"'])
            await ctx.send("Minecraft rebooted. please wait for the proxy to turn on")
        except:
            #If there is an error, log it and tell the user
            Level= "Severe"
            Reason= "Minecraft failed to restart"
            await ctx.send("Minecraft Failed to restart")
            LogError(Level,Reason)
        pass
    @MCrestart.error
    async def MCrestartError(self ,ctx ,error):
        global person
        if isinstance(error, commands.CheckFailure):
            person= ctx.author
            personID= person.id
            person= str(person)
            personID= str(personID)
            Level= "Warn"
            Reason= ("Unauthorised Minecraft reboot attempted by",person)
            await ctx.send("You dont have permissions ("+Adminrole+") to do this <@"+personID+">")
            LogError(Level,Reason)


    #This creates a backup of the minecraft server
    #@commands.command(pass_context=True)
    #@commands.has_role(Adminrole)
    #async def MCbackup(self ,ctx):

    #    global person
     #   person= ctx.author
      #  person= str(person)
    #    print("Minecraft Backedup by "+ person)
    #    await ctx.send("Backing up Minecraft...")
    #    with open (Generallog, "a") as log:
    #        currenttime= str(time.strftime("%Y-%m-%D %H:%M:%S", time.localtime()))
    #        log.write(currenttime+ "   Minecraft Backed up by "+ person+"\n")
    #    log.close
    #    try:
    #        #more MC commands for the tmux session
    #        subprocess.run(["sudo","-u","server","tmux", "send-keys", "-t", "Minecraft", "ENTER"])
    #        #turns off automatic saving on the minecraft server so the backup is not corrupted
    #        subprocess.run(["sudo","-u","server","tmux", "send-keys", "-t", "Minecraft", "/save-off", "ENTER"])
    #        #Spilitting time and becoming a time lord
#
     #       day = str(time.strftime("%Y-%m-%D", time.localtime()))
            #print("Dating done")
     #       Minecraftbackupfilepath=("/opt/backups/minecraft/"+gametype+"/"+version) #Change this to the filepath of your minecraft server backups
     #       print("checking filepath")
    #        backupfile_exists = os.path.isdir(Minecraftbackupfilepath+"/"+day)
    #        print(backupfile_exists)
    #        Minecraftbackupfilepath= os.path.join(Minecraftbackupfilepath,day)
    #        if backupfile_exists== False:
            #    print("New day making")
    #            #Creates a new folder for the backup if its a new day
    #            print("attempting to create a filepath")
                #subprocess.run(["sudo","mkdir",Minecraftbackupfilepath])
   #             print("filepath created")

            #    print("New day made")
            #print("Datechecked/made")
            #More time lord stuff
    #        hour= str(time.strftime("%H", time.localtime()))
     #       print(hour)
            #print("Hours calculated")
    #        backupfilepath= os.path.join(Minecraftbackupfilepath,hour)
    #        print("checking filepath")
    #        backupfile_exists = os.path.isdir(backupfilepath)
    #        print(backupfile_exists)
            #print("Hours checked")
    #        if backupfile_exists== False:
    #            Minecraftbackupfilepath= os.path.join(Minecraftbackupfilepath,hour)
                #print("Hour joined")
                #makes the backup under the hour and minute
     #           print("attempting to create a filepath")
     ##           #subprocess.run(["sudo","mkdir",backupfilepath])
     #           print("filepath created")
                #print("File made")
    #            #subprocess.run(["sudo","cp",Minecraftserverfilepath+"/world",backupfilepath+"/world/","-rf"])
                #print("copied over the files")
                #turns on automatic saving on the minecraft server as the backup is done
                #subprocess.run(["sudo","-u","server","tmux", "send-keys", "-t", "Minecraft", "/save-on", "ENTER"])
     #           await ctx.send("Minecraft backed up succesfully")
     #           print(Minecraftbackupfilepath,backupfilepath)
     #       else:
                #print("Backup already exists so fuck you")
                #Boo-hoo the backup already existed in that minute so why the fuck are you making another
     #           subprocess.run(["sudo","-u","server","tmux", "send-keys", "-t", "Minecraft", "/save-on", "ENTER"])
     #   except:
            #error catching and logging
     #       Level= "Severe"
     #       Reason= "Minecraft failed to Backup"
     #       await ctx.send("Minecraft Failed to Backup")
     #       LogError(Level,Reason)
     #       #turns on saving so it doesnt stay off if there is an error
      #      subprocess.run(["sudo","-u","server","tmux", "send-keys", "-t", "Minecraft", "/save-on", "ENTER"])
     #       pass
        pass
    #Incase someone doesnt have permissions
    #@MCbackup.error
    #async def MCbackupError(self ,ctx ,error):
    #    global person
    #    if isinstance(error, commands.CheckFailure):
    #        person= ctx.author
    #        personID= person.id
    #        person= str(person)
    #        personID= str(personID)
    #        Level= "Warn"
    #        Reason= ("Unauthorised Minecraft Backup attempted by",person)
    #        await ctx.send("You dont have permissions ("+Adminrole+") to do this <@"+personID+">")
    #        LogError(Level,Reason)

async def setup(bot):
      await bot.add_cog(minecraft(bot))