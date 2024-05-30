# bot.py
import os
import os.path
from tokenize import Token
from tracemalloc import start
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
person= ""
TOKEN = "MTI0MDcyMTgwNTY5ODY2MjU2MQ.GHqu2I.M15rcqb8jebTDBzo8zdamsYDitHcuqN3UhOaZ8"
SystemChannelID= 1240997501750743221
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is ready\n\n")
    currenttime= str(datetime.now())
    SystemChannel= bot.get_channel(SystemChannelID)
    
    await SystemChannel.send("Bot is ACTIVE at "+currenttime)
    with open ("./ImportantTxtfiles/Logs.txt", "a") as log:
        currenttime= str(datetime.now())
        log.write("\n"+currenttime+ "   Bot Started\n")
    log.close()

@bot.command()
async def hi(ctx):
    personID= ctx.author.id
    personID= str(personID)
    #await ctx.send("Hey")
    await ctx.send("Hey <@"+personID+">")



@bot.command(pass_context=True)
@commands.has_role("BotKing")
async def restart(ctx):
    global person
    person= ctx.author
    person= str(person)
    print("Bot restarted by "+ person)
    await ctx.send("Restarting...")
    with open ("./ImportantTxtfiles/Logs.txt", "a") as log:
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
        with open ("./ImportantTxtfiles/Logs.txt", "a") as log:
            currenttime= str(datetime.now())
            log.write(currenttime+ "   (FAIL) Bot Restart attempted by "+ person+"\n")
        log.close()
        await ctx.send("You dont have permissions (BotKing) to do this <@"+personID+">")
        

@bot.command(pass_context=True)
@commands.has_role("BotKing")
async def shutdown(ctx):
    global person
    person= ctx.author
    person= str(person)
    print("Bot Shutdown by "+ person)
    await ctx.send("Shutting down...")
    with open ("./ImportantTxtfiles/Logs.txt", "a") as log:
        currenttime= str(datetime.now())
        log.write(currenttime+ "   Bot Shutdown by "+ person+"\n")
    log.close()
    while True:
        await bot.change_presence(status=discord.Status.invisible)
        time.sleep(1)
        await exit()
    
@shutdown.error
async def shutdownError(ctx ,error):
    global person
    if isinstance(error, commands.CheckFailure):
        person= ctx.author
        personID= person.id
        person= str(person)
        personID= str(personID)
        with open ("./ImportantTxtfiles/Logs.txt", "a") as log:
            currenttime= str(datetime.now())
            log.write(currenttime+ "   (FAIL) Bot Shutdown attempted by "+ person+"\n")
        log.close()
        await ctx.send("You dont have permissions (BotKing) to do this <@"+personID+">")
        

Bullets= 0
playerRR= 0
HighScoreRR= 0
PlayerlistRR= []
GameRR= []

@bot.command()
async def RussianRoulette(ctx):
    global HighScoreRR
    global Bullets
    global playerRR
    global ContinueResponseRR
    async def RRgame():
        BulletsRR= [1]
        global GameRR
        global scoreRR
        global Dude
        scoreRR= 0
        scoreRR= str(scoreRR)
        print("hi")
        
        print("part 1 complete")
        async def BulletCreation():
            print("1")
            global BulletsRR
            BulletsRR= [1]
            print("2")
            for i in range(random.randint(1,5)):
                print("3")
                BulletsRR.append(0)
                print("4")
            random.shuffle(BulletsRR)
            print("5")
            await ctx.send("The ammount of Bullets in the revolver is", len(BulletsRR))
            BulletsRR= "|".join(BulletsRR)
            print("part 2 complete")
            for i in range(len(GameRR)):
                if Dude== GameRR[i][0]:
                    BulletsRR= GameRR[i][2]
                    success= True
            if success== False:
                print("error")
            else:
                print("part 3 complete")
                PlayerChoosing()
        await BulletCreation()
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
        with open ("./ImportantTxtfiles/Logs.txt", "a") as log:
            currenttime= str(datetime.now())
            log.write(currenttime+ "   (Game) "+ Dude+"Has started playing Russian Roulette")
        log.close()
        playerRR= Dude
        PlayerlistRR.append(Dude)
        print(Dude,"Added to Russian Roulette")
        file_exists = os.path.exists('./RussianRouletteFiles/'+playerRR+'.csv')
        if file_exists== True:
                with open('./RussianRouletteFiles/'+playerRR+'.csv',"r") as Game: 
                    reader= csv.reader(Game)
                    for row in reader:
                        ActiveGame= row[0]
                        HighScoreRR= row[1]
                        HighScoreRR= int(HighScoreRR)
                        if ActiveGame== "True":
                            Bullets= row[2]
                Game.close
        else:
            with open('./RussianRouletteFiles/'+playerRR+'.csv',"w") as Game:
                writer=csv.writer(Game, lineterminator= "\n")
                writer.writerow(["False","1"])
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
                                i= i+1
                        except:   
                            i=0
        else:
            GameRR.append([playerRR])        
            await ctx.send("starting new game...")
            await RRgame()

    else:
        await ctx.send("you are already playing")

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
                    with open ("./ImportantTxtfiles/Logs.txt", "a") as log:
                        currenttime= str(datetime.now())
                        log.write(currenttime+ "   (Game) "+ str(ctx.author)+"Has stopped playing Russian Roulette")
                    log.close()
                    print("Quit successful ("+str(ctx.author)+")")
                    await ctx.send("Quit Successful")
                    Quitting= True

    if Quitting== False:
        print("Couldn't quit (Person not playing)("+str(ctx.author)+")")
        await ctx.send("Couldn't quit (Person not playing)")
        


bot.run(TOKEN)