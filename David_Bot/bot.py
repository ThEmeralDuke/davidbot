# bot.py
import os
import os.path
import discord
from discord import *
from discord.ext import commands
from discord.utils import *
import time
import datetime
from datetime import *
from subprocess import Popen
import csv
import random
filepath= (r"C:\Users\matty\Documents\Visual Studio 2022\Repos\ThEmeralDuke\David_Bot\David_Bot") # make this your file path
person= ""
with open (filepath+"/ImportantTxtfiles/important.csv", "r") as info:
    reader= csv.reader(info)
    for row in reader:
        TOKEN= row[0]
        Adminrole=row[1]
info.close()

SystemChannelID= 1240997501750743221
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is ready\n\n")
    currenttime= str(datetime.now())
    SystemChannel= bot.get_channel(SystemChannelID)
    
    await SystemChannel.send("Bot is ACTIVE at "+currenttime)
    with open (filepath+"/ImportantTxtfiles/Logs.log", "a") as log:
        currenttime= str(datetime.now())
        log.write("\n"+currenttime+ "   Bot Started\n")
    log.close()

@bot.command()
async def hi(ctx):
    await bot.change_presence(status=discord.Status.online)
    personID= ctx.author.id
    personID= str(personID)
    #await ctx.send("Hey")
    await ctx.send("Hey <@"+personID+">")



@bot.command(pass_context=True)
@commands.has_role(Adminrole)
async def restart(ctx):
    global person
    person= ctx.author
    person= str(person)
    print("Bot restarted by "+ person)
    await ctx.send("Restarting...")
    with open (filepath+"/ImportantTxtfiles/Logs.log", "a") as log:
        currenttime= str(datetime.now())
        log.write(currenttime+"   Bot Restarted by "+ person+"\n")
    log.close()
    await bot.change_presence(status=discord.Status.do_not_disturb)
    Popen('python restart.py')
    exit()
    

@restart.error
async def restartError(ctx ,error):
    global person
    if isinstance(error, commands.CheckFailure):
        person= ctx.author
        personID= person.id
        person= str(person)
        personID= str(personID)
        with open (filepath+"/ImportantTxtfiles/Logs.log", "a") as log:
            currenttime= str(datetime.now())
            log.write(currenttime+ "   (FAIL) Bot Restart attempted by "+ person+"\n")
        log.close()
        await ctx.send("You dont have permissions ("+Adminrole+") to do this <@"+personID+">")
        

@bot.command(pass_context=True)
@commands.has_role("BotKing")
async def shutdown(ctx):
    global person
    person= ctx.author
    person= str(person)
    print("Bot Shutdown by "+ person)
    await ctx.send("Shutting down...")
    with open (filepath+"/ImportantTxtfiles/Logs.log", "a") as log:
        currenttime= str(datetime.now())
        log.write(currenttime+ "   Bot Shutdown by "+ person+"\n")
    log.close()
    while True:
        await bot.change_presence(status=discord.Status.invisible)
        time.sleep(1)
        w = 0/0
        print(w)
    
@shutdown.error
async def shutdownError(ctx ,error):
    global person
    if isinstance(error, commands.CheckFailure):
        person= ctx.author
        personID= person.id
        person= str(person)
        personID= str(personID)
        with open (filepath+"/ImportantTxtfiles/Logs.log", "a") as log:
            currenttime= str(datetime.now())
            log.write(currenttime+ "   (FAIL) Bot Shutdown attempted by "+ person+"\n")
        log.close()
        await ctx.send("You dont have permissions ("+Adminrole+") to do this <@"+personID+">")







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
        with open (filepath+"/ImportantTxtfiles/Logs.log", "a") as log:
            currenttime= str(datetime.now())
            log.write(currenttime+ "   (Game) "+ Dude+"Has started playing Russian Roulette\n")
        log.close()
        playerRR= Dude
        PlayerlistRR.append(Dude)
        print(Dude,"Added to Russian Roulette")
        file_exists = os.path.exists('./RussianRouletteFiles/'+playerRR+'.csv')
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
        if ActiveGame== "True":
                    await ctx.send("You have an active game <@"+DudeID+">\nWould you like to continue it? #yes #no")
                    GameRR.append([playerRR,Bullets,HighScoreRR,"response"])
                    options = ["yes", "no"]
                    def check(m):
                        return (
                            m.content.startswith("#")
                            and m.content.lower()[1:] in options
                            and m.channel.id == ctx.channel.id
                            and m.author.id== ctx.author.id
                        )
                    i=0    
                    while True:
                        msg = await bot.wait_for("message", check=check)
                        try:
                            if Dude== GameRR[i][0] and GameRR[i][3]== "response":
                                if str(msg.content).lower()== "#yes":
                                    await ctx.send("Loading game...")
                                    del GameRR[i][3]
                                    index= i
                                    await RRgame()
                                    break
                                else:
                                    await ctx.send("starting new game...")
                                    del GameRR[i][3],  GameRR[i][2],
                                    await RRgame()
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
                    with open (filepath+"/ImportantTxtfiles/Logs.log", "a") as log:
                        currenttime= str(datetime.now())
                        log.write(currenttime+ "   (Game) "+ str(ctx.author)+"Has stopped playing Russian Roulette\n")
                    log.close()
                    print("Quit successful ("+str(ctx.author)+")")
                    await ctx.send("Quit Successful")
                    Quitting= True

    if Quitting== False:
        print("Couldn't quit (Person not playing)("+str(ctx.author)+")")
        await ctx.send("Couldn't quit (Person not playing)")
        


bot.run(TOKEN)