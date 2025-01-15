filepath= (r".")
Errorlog= filepath+"/ImportantTxtfiles/Logs/Error.log"
def LogError(Level,Reason):
    with open (Errorlog, "a") as log:
            currenttime= str(datetime.now())
            log.write(f"{currenttime}    ({Level}) {Reason}\n")
    log.close()
Resourcelog= filepath+"/ImportantTxtfiles/Logs/Resource.log"
def LogResource(Level,Reason,Percent):
    with open (Resourcelog, "a") as log:
            currenttime= str(datetime.now())
            log.write(f"{currenttime}    ({Level}) {Reason} at {Percent}%\n")
    log.close()
import os
import os.path
from dotenv import *
import discord
from discord import *
from discord.ext import commands
from discord.utils import *
import time as timee
import datetime
from datetime import *
import csv
import random
import threading
import subprocess
import psutil
botrole= []
Adminrole= []
person= ""
Generallog= filepath+"/ImportantTxtfiles/Logs/General.log"
LocalFilepath= "/home/server/" #Change this to your local devices filepath
load_dotenv(filepath+"/ImportantTxtfiles/.env")
with open (filepath+"/ImportantTxtfiles/important.csv", "r") as info:
    reader= csv.reader(info)
    for row in reader:
        botrole= row[0]
        Adminrole=row[1]
info.close()


with open (filepath+"/ImportantTxtfiles/settings.csv", "r") as settings:
    reader= csv.reader(settings)
    for row in reader:
        LeaderboardDelay= row[0]
        LeaderboardDelay= int(LeaderboardDelay)
        gametype= str(row[1])
        version= str(row[2])
settings.close()

##Minecraft settings##

Minecraftserverfilepath=("/opt/minecraft") #Change this to the filepath of your minecraft server
Minecraftbackupfilepath=("/opt/backups/"+gametype+"/"+version) #Change this to the filepath of your minecraft server backups

##

#SystemChannelID= 1240997501750743221 #This should be the test channel for your bot to see if it starts (delete if unnessecary)
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), activity = discord.Activity(type=discord.ActivityType.listening, name="!Commands"))

def Warningsystem():
    while True:
        memory_info = psutil.virtual_memory()
        rampercent= float(f"{memory_info.percent}")
        cpu_util = psutil.cpu_percent(interval=1)
        if rampercent >=95:
            print(f"(Critical) Ram usage Very high ({rampercent}%)")
            level="Critical"
            reason="RAM"
            LogResource(level,reason,rampercent)
        elif rampercent >=85:
            print(f"(Serious) Ram usage high ({rampercent}%)")
            level="Serious"
            reason="RAM"
            LogResource(level,reason,rampercent)
        elif rampercent >=75:
            print(f"(Warning) Ram usage getting high ({rampercent}%)")
            level="Warning"
            reason="RAM"
            LogResource(level,reason,rampercent)
        if cpu_util >=95:
            print(f"(Critical) CPU usage Very high ({cpu_util}%)")
            level="Critical"
            reason="CPU"
            LogResource(level,reason,cpu_util)
        elif cpu_util >=85:
            print(f"(Serious) CPU usage high ({cpu_util}%)")
            level="Serious"
            reason="CPU"
            LogResource(level,reason,cpu_util)
        elif cpu_util >=75:
            print(f"(Warning) CPU usage getting high ({cpu_util}%)")
            level="Warning"
            reason="CPU"
            LogResource(level,reason,cpu_util)
        timee.sleep(20)


@bot.command()
async def Commands(ctx):
    person= ctx.author
    personID= person.id
    person= str(person)
    personID= str(personID)
    await ctx.send("List of commands: (Case sensitive)\n1. !hi\n2. !Usage\n3. !Reboot (admin protected)\n4. !MCrestart (admin protected)\n5. !MCbackup (admin protected)\n6. !startRR\n7. !RRleaderboard\n8. !QuitRR\n\n<@"+personID+">")
@bot.event
async def on_ready():
    print("Bot is ready\n\n")
    currenttime= str(datetime.now())
    #SystemChannel= bot.get_channel(SystemChannelID)
    
    #await SystemChannel.send("Bot is ACTIVE at "+currenttime)
    with open (Generallog, "a") as log:
        currenttime= str(datetime.now())
        log.write("\n"+currenttime+ "   Bot Started\n")
    log.close()

@bot.command()
async def hi(ctx):
    await bot.change_presence(status=discord.Status.online)
    personID= ctx.author.id
    personID= str(personID)
    await ctx.send("Hey <@"+personID+">")

@bot.command()
async def Usage(ctx):
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


@bot.command(pass_context=True)
@commands.has_role(Adminrole)
async def reboot(ctx):

    global person
    person= ctx.author
    person= str(person)
    print("Bot rebooted by "+ person)
    await ctx.send("rebooting...")
    with open (Generallog, "a") as log:
        currenttime= str(datetime.now())
        log.write(currenttime+ "   Bot rebooted by "+ person+"\n")
    log.close()
    while True:
        await bot.change_presence(status=discord.Status.invisible)
        subprocess.run(["sudo", "reboot"])
        exit()
    pass
@reboot.error
async def rebootError(ctx ,error):
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


Minecraftserverfilepath="/opt/minecraft" #Change this to the filepath of your minecraft server
Minecraftbackupfilepath="/opt/backups/"+gametype+"/"+version+"/" #Change this to the filepath of your minecraft server backups
@bot.command(pass_context=True)
@commands.has_role(Adminrole)
async def MCrestart(ctx):

    global person
    person= ctx.author
    person= str(person)
    print("Minecraft rebooted by "+ person)
    await ctx.send("Restarting Minecraft...")
    with open (Generallog, "a") as log:
        currenttime= str(datetime.now())
        log.write(currenttime+ "   Minecraft restarted by "+ person+"\n")
    log.close
    try:
        try:
            subprocess.run(["sudo","-u","server","tmux", "send-keys", "-t", "Minecraft", "/stop", "ENTER"])
        except:
            pass
        timee.sleep(3)
        result = subprocess.run(
                ["sudo", "-u", "server", "/bin/bash", "/home/server/sh/mcstart.sh"], 
                check=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
                )
        pass
    except:
        Level= "Severe"
        Reason= "Minecraft failed to restart"
        await ctx.send("Minecraft Failed to restart")
        LogError(Level,Reason)
        pass
    pass
@MCrestart.error
async def MCrestartError(ctx ,error):
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

@bot.command(pass_context=True)
@commands.has_role(Adminrole)
async def MCbackup(ctx):

    global person
    person= ctx.author
    person= str(person)
    print("Minecraft Backedup by "+ person)
    await ctx.send("Backing up Minecraft...")
    with open (Generallog, "a") as log:
        currenttime= str(datetime.now())
        log.write(currenttime+ "   Minecraft Backed up by "+ person+"\n")
    log.close
    try:
        subprocess.run(["sudo","-u","server","tmux", "send-keys", "-t", "Minecraft", "/save-off", "ENTER"])
        datew= str(datetime.today())
        datew= datew.split()
        day = str(datew[0])
        Minecraftbackupfilepath=("/opt/backups/"+gametype+"/"+version) #Change this to the filepath of your minecraft server backups
        backupfile_exists = os.path.isdir(Minecraftbackupfilepath+"/"+day)
        datew= datew[1].split(".")
        hour=str((datew[0]))
        hour=hour.split(":")
        hour=hour[0]+":"+hour[1]
        Minecraftbackupfilepath= (Minecraftbackupfilepath+"/"+day)
        backupfilepath= Minecraftbackupfilepath+"/"+hour
        backupfile_exists = os.path.isdir(backupfilepath)
        if backupfile_exists== False:
            os.mkdir(Minecraftbackupfilepath+"/"+hour)
            subprocess.run(["sudo","cp",Minecraftserverfilepath+"/world",Minecraftbackupfilepath+"/"+hour+"/","-rf"])
            subprocess.run(["sudo","-u","server","tmux", "send-keys", "-t", "Minecraft", "/save-on", "ENTER"])
        else:
            print("Backup already exists so fuck you")
            subprocess.run(["sudo","-u","server","tmux", "send-keys", "-t", "Minecraft", "/save-on", "ENTER"])
            crash=0/0
            print(crash)
    except:
        Level= "Severe"
        Reason= "Minecraft failed to Backup"
        await ctx.send("Minecraft Failed to Backup")
        LogError(Level,Reason)
        pass
    pass
@MCbackup.error
async def MCbackupError(ctx ,error):
    global person
    if isinstance(error, commands.CheckFailure):
        person= ctx.author
        personID= person.id
        person= str(person)
        personID= str(personID)
        Level= "Warn"
        Reason= ("Unauthorised Minecraft Backup attempted by",person)
        await ctx.send("You dont have permissions ("+Adminrole+") to do this <@"+personID+">")
        LogError(Level,Reason)

#######      RUSSIAN ROULETTE      ######

scoreRR= 0
playerRR= 0
HighScoreRR= 0
PlayerlistRR= []
GameRR= []
@bot.command()
async def startRR(ctx):
    global HighScoreRR
    global Bullets
    global mcontext
    global playerRR
    global ContinueResponseRR
    found= False
    ActiveGame="False"
    Dude= ctx.author
    DudeID= Dude.id
    DudeID= str(DudeID)
    Dude= str(Dude)
    for index in range(len(PlayerlistRR)):
        if found== False:    
            if PlayerlistRR[index] == Dude:
                found= True
                print(Dude, "found")
    if found== False:
        with open (Generallog, "a") as log:
            currenttime= str(datetime.now())
            log.write(currenttime+ "   (Game) "+ Dude+"Has started playing Russian Roulette\n")
        log.close()
        playerRR= Dude
        PlayerlistRR.append(Dude)
        print(Dude,"Added to Russian Roulette")
        try:
            os.mkdir(filepath+"/RussianRouletteFiles")
        except:
            pass
        file_exists = os.path.exists(filepath+'/RussianRouletteFiles/'+playerRR+'.csv')
        if file_exists== True:
                with open(filepath+'/RussianRouletteFiles/'+playerRR+'.csv',"r") as Game: 
                    reader= csv.reader(Game)
                    for row in reader:
                        HighScoreRR= row[0]
                        HighScoreRR= int(HighScoreRR)
                Game.close
        else:
            with open(filepath+'/RussianRouletteFiles/'+playerRR+'.csv',"w") as Game:
                writer=csv.writer(Game, lineterminator= "\n")
                writer.writerow(["0"])
            Game.close
        GameRR.append([playerRR,HighScoreRR,0])        
        print(Dude,"Loaded")
        
        await ctx.send("Loaded. Please use !RRgame to start")

    else:
        await ctx.send("you are already playing")
scoreRR= 0        
@bot.command()
async def RRgame(ctx):
    
    global scoreRR
    global GameRR
    global BulletsRR
    Dude= ctx.author
    DudeID= Dude.id
    DudeID= str(DudeID)
    Dude= str(Dude)
    for o in range(len(GameRR)):
        if GameRR[o][0]== Dude:
            await ctx.send("That command can be used to restart the game")
            with open(filepath+'/RussianRouletteFiles/'+playerRR+'.csv',"r") as Game: 
                reader= csv.reader(Game)
                for row in reader:
                    HighScoreRR= row[0]
                    HighScoreRR= int(HighScoreRR)
                    GameRR[o][1]= HighScoreRR
            Game.close
            BulletsRR= [1]
            global scoreRR
            Dude= ctx.author
            DudeID= Dude.id
            DudeID= str(DudeID)
            Dude= str(Dude)
            BulletsRR= [1]
            for i in range(random.randint(1,5)):
                BulletsRR.append(0)
            random.shuffle(BulletsRR)
            print("shuffled")
            msg= "The ammount of Bullets in the revolver is ", str(len(BulletsRR))
            msg= ("".join(msg))
            await ctx.send(msg)
            print("part 2 complete")
            try:
                del GameRR[o][3]
                try:
                    del GameRR[o][3]
                except:
                    print()
            except:
                print()
            GameRR[o].append(BulletsRR)
            GameRR[o].append("response")
            print(GameRR)
            await ctx.send("Are you going to shoot yourself or shoot the dealer? (send !S or !D) ")

@bot.command()
async def S(ctx):
    global scoreRR
    global GameRR
    Dude= ctx.author
    DudeID= Dude.id
    DudeID= str(DudeID)
    Dude= str(Dude)
    global BulletsRR
    for y in range(len(GameRR)):
        try:
            if GameRR[y][0]== Dude and GameRR[y][4]== "response":
                print(Dude,"chose to shoot themselves")
                del GameRR[y][4]
                if GameRR[y][3][0]== 1:
                    await ctx.send("You died...")
                    #end
                    if int(GameRR[y][2])== 0:
                        await ctx.send("L bozo")
                    
                    elif int(GameRR[y][2]) > GameRR[y][1]:
                        with open(filepath+'/RussianRouletteFiles/'+playerRR+'.csv',"w") as Game:
                            writer=csv.writer(Game, lineterminator= "\n")
                            writer.writerow([GameRR[y][2]])
                            Game.close()
                    GameRR[y][2]= 0    
                else:
                    await ctx.send("Blank")

                    del GameRR[y][3][0]
                    print(GameRR[y][3])
                    if GameRR[y][3]== []:
                        await ctx.send("No one died")
                        timee.sleep(1)
                        await ctx.send("Please use !RRgame to go to next game")
                        del GameRR[y][3], 
                    
                    else:
                        await ctx.send("Are you going to shoot yourself or shoot the dealer? (send !S or !D) ")
                        GameRR[y].append("response")
        except:
            await ctx.send("Please use !RRgame to start the game")
@bot.command()
async def D(ctx):
    global scoreRR
    global GameRR
    Dude= ctx.author
    DudeID= Dude.id
    DudeID= str(DudeID)
    Dude= str(Dude)
    global BulletsRR
    for y in range(len(GameRR)):
        try:
            if GameRR[y][0]== Dude and GameRR[y][4]== "response":
                print(Dude,"chose to shoot the Dealer")
                del GameRR[y][4]
                if GameRR[y][3][0]== 1:
                    await ctx.send("The Dealer is dead")
                    int(GameRR[y][2])
                    GameRR[y][2]= GameRR[y][2]+1
                    if GameRR[y][2] > GameRR[y][1]:
                        with open(filepath+'/RussianRouletteFiles/'+playerRR+'.csv',"w") as Game:
                            writer=csv.writer(Game, lineterminator= "\n")
                            writer.writerow([GameRR[y][2]])
                            Game.close()
                    await ctx.send("Please use !RRgame to go to next game")
                else:
                    print("Blank")
                    del GameRR[y][3][0]
                    print(GameRR[y][3])
                    if GameRR[y][3][0]== []:
                        timee.sleep(1)
                        await ctx.send("Please use !RRgame to go to next game")
                    else:
                    

                        #####dealer#####

                        while True:
                            print("Dealer is choosing for",Dude)
                            if GameRR[y][3][0]== [1]:
                                DealersChoice= 1
                            else:
                                DealersChoice= random.randint(1,4)
                            if DealersChoice== 4:
                                await ctx.send("Dealer is choosing to shoot themself")
                                if GameRR[y][3][0]== 1:
                                    await ctx.send("The Dealer is dead")
                                    int(GameRR[y][2])
                                    GameRR[y][2]= GameRR[y][2]+1
                                    if GameRR[y][2] > GameRR[y][1]:
                                        with open(filepath+'/RussianRouletteFiles/'+playerRR+'.csv',"w") as Game:
                                            writer=csv.writer(Game, lineterminator= "\n")
                                            writer.writerow([GameRR[y][2]])
                                            Game.close()
                                    await ctx.send("Please use !RRgame to go to next game")
                                    break
                                else:
                                    await ctx.send("Blank")

                                    del GameRR[y][3][0]
                                    print(GameRR[y][3])
                                    if GameRR[y][3][0]== []:
                                        await ctx.send("No one died...")
                                        await ctx.send("Please use !RRgame to go to next game")
                                    await ctx.send("Are you going to shoot yourself or shoot the new dealer? (send !S or !D) ")
                                    GameRR[y].append("response")
                                    break
                            elif DealersChoice== 1 or DealersChoice== 2 or DealersChoice== 3:
                                await ctx.send("Dealer is choosing to shoot you")
                                if GameRR[y][3][0]== 1:
                                    await ctx.send("You died...")
                                    #end
                                    if int(GameRR[y][2])== 0:
                                        await ctx.send("L bozo")
                    
                                    elif int(GameRR[y][2]) > GameRR[y][1]:
                                        with open(filepath+'/RussianRouletteFiles/'+playerRR+'.csv',"w") as Game:
                                            writer=csv.writer(Game, lineterminator= "\n")
                                            writer.writerow([GameRR[y][2]])
                                            Game.close()
                                    GameRR[y][2]= 0
                                    break
                                else:
                                    await ctx.send("Blank")

                                    del GameRR[y][3][0]
                                    if GameRR[y][3][0]== []:
                                        await ctx.send("No one died...")
                                        await ctx.send("Please use !RRgame to go to next game")
                                    else:
                                        await ctx.send("Are you going to shoot yourself or shoot the new dealer? (send !S or !D) ")
                                        GameRR[y].append("response")
                                    break
        except:
            await ctx.send("Please use !RRgame to start the game")

RrLBoardToggle= True     
RRtimer= 0
def TimerLeaderboard():
    global RrLBoardToggle
    global RRtimer
    while True:
        timee.sleep(1)
        RRtimer= RRtimer+1
        if RRtimer>= LeaderboardDelay:
            print("RR leaderboard is useable again")
            RrLBoardToggle= True
            RRtimer= 0
            break


RRLBcontinue= False
LeaderboardListRR= []
@bot.command()
async def RRleaderboard(ctx):
    global LeaderboardListRR
    global RrLBoardToggle
    global RRLBcontinue
    person= ctx.author
    personID= person.id
    person= str(person)
    personID= str(personID)
    LeaderboardListRR= []
    if RrLBoardToggle== True:
        RrLBoardToggle= False
        RRtimethread = threading.Thread(target=TimerLeaderboard)
        RRtimethread.start()
        bannedrole = discord.utils.get(ctx.guild.roles, name=botrole)
        n=0
        for member in ctx.guild.members:
            #try:
            if bannedrole in member.roles:
                pass
            else:
                n=n+1
                Dude= member.name
                Dude= str(Dude)
                LeaderboardListRR.append([Dude])
            #except:
                pass
        RRLBcontinue= False
        RRlboardthread = threading.Thread(target=checkRRfiles, args=(ctx,))
        RRlboardthread.start()
        while RRLBcontinue== False:
            pass
        RRlboardthread.join()
        # Sort the 2D array based on the second column (index 1)
        arr= LeaderboardListRR
        col_index= 1
        insertion_sort_2d_Descending(arr, col_index)
        continueIS2D= False 
        print(arr)
        try:
            msg= "These are the 3 best people at Russian Roulette\n1. ",str(arr[0][0])," with ",str(arr[0][1])," points\n2. ",str(arr[1][0])," with ",str(arr[1][1])," points\n3. ",str(arr[2][0])," with ",str(arr[2][1])," points\n<@"+personID+">"
            
            msg= ("".join(msg))
            await ctx.send(msg)
        except:
            try:
                msg= "These are the 2 best people at Russian Roulette\n1. ",str(arr[0][0])," with ",str(arr[0][1])," points\n2. ",str(arr[1][0])," with ",str(arr[1][1])," points\n<@"+personID+">"
                msg= ("".join(msg))
                await ctx.send(msg)
            except:
                msg= "This is the best at Russian Roulette\n1. ",str(arr[0][0])," with ",str(arr[0][1])," points\n<@"+personID+">"
                msg= ("".join(msg))
                await ctx.send(msg)
    else:
        await ctx.send("Please wait until ("+str(LeaderboardDelay)+") second(s) have passed since last leaderboard request")

def checkRRfiles(ctx,):
    global LeaderboardListRR
    global RRLBcontinue
    b=0
    for member in ctx.guild.members:
        try:
            try:
                with open(filepath+'/RussianRouletteFiles/'+LeaderboardListRR[b][0]+'#0.csv',"r") as listing: 
                    reader= csv.reader(listing)
                    for row in reader:
                        HighScoreRR= row[0]
                        HighScoreRR= int(HighScoreRR)
                listing.close
                LeaderboardListRR[b].append(HighScoreRR)
                #print("fit")
            except:
                #print("unfit")
                LeaderboardListRR[b].append(0)
                pass
            b=b+1
        except:
            b=0
    RRLBcontinue=True
    print("Collected data for leaderboard")



@bot.command()
async def QuitRR(ctx):
    global GameRR
    global PlayerlistRR
    Quitting= False
    for i in range(len(GameRR)):
        if str(ctx.author) == GameRR[i][0]:
            del GameRR[i]
            for u in range(len(PlayerlistRR)):
                if str(ctx.author) == PlayerlistRR[u]:
                    del PlayerlistRR[u]
                    with open (Generallog, "a") as log:
                        currenttime= str(datetime.now())
                        log.write(currenttime+ "   (Game) "+ str(ctx.author)+"Has stopped playing Russian Roulette\n")
                    log.close()
                    print("Quit successful ("+str(ctx.author)+")")
                    await ctx.send("Quit Successful")
                    Quitting= True

    if Quitting== False:
        print("Couldn't quit (Person not playing)("+str(ctx.author)+")")
        await ctx.send("Couldn't quit (Person not playing)")


####    MISC    ####

continueIS2D= False
col_index= 0
def insertion_sort_2d_Descending(arr, col_index):
    try:
        
        global continueIS2D
        continueIS2D= False
        # Traverse through 1 to len(arr)
        try:
            for i in range(1, len(arr)):
                key = arr[i]
                j = i - 1
        
                # Move elements of arr[0..i-1], that are greater than key,
                # to one position ahead of their current position
                while j >= 0 and arr[j][col_index] < key[col_index]:
                    arr[j + 1] = arr[j]
                    j -= 1
                arr[j + 1] = key
        except:

            return arr
            pass
    except:
        Level= "Severe"
        Reason= "Bot failed to do the 2d sort"
        LogError(Level,Reason)
        pass

Warningsystemthread= threading.Thread(target=Warningsystem)
Warningsystemthread.start()
bot.run(str(os.getenv("BOT_KEY"))) #rename this to what your bot token variable is called in your .env file

