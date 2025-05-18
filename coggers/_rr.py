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
import random
import threading
import json
import asyncio

#stuff
botrole= []
Adminrole= []
person= ""
Generallog= filepath+"/ImportantTxtFiles/Logs/General.log"
LocalFilepath= "/home/server/" #Change this to your local devices filepath
load_dotenv(filepath+"/ImportantTxtFiles/.env")
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
scoreRR= 0
playerRR= 0
HighScoreRR= 0
PlayerlistRR= []
GameRR= []
class rr(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    @commands.Cog.listener()
    async def on_ready(self):
         print("rr.py is ready")
    


    #######      RUSSIAN ROULETTE      ######


    @commands.command()
    async def startRR(self,ctx):
        print("Seen")
        global HighScoreRR
        global playerRR
        global PlayerlistRR
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
            print("sen2")
            with open (Generallog, "a") as log:
                currenttime= str(time.strftime("%Y-%m-%D %H:%M:%S", time.localtime()))
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
                    Game.close()
            else:
                with open(filepath+'/RussianRouletteFiles/'+playerRR+'.csv',"w") as Game:
                    writer=csv.writer(Game, lineterminator= "\n")
                    writer.writerow(["0"])
                Game.close()
            GameRR.append([playerRR,HighScoreRR,0])        
            print(Dude,"Loaded")
            
            await ctx.send("Loaded. Please use !RRgame to start")

        else:
            await ctx.send("you are already playing")

    scoreRR= 0    

    @commands.command()
    async def RRgame(self,ctx):
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
                Game.close()
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

    @commands.command()
    async def S(self,ctx):
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
                            time.sleep(1)
                            await ctx.send("Please use !RRgame to go to next game")
                            del GameRR[y][3], 
                        
                        else:
                            await ctx.send("Are you going to shoot yourself or shoot the dealer? (send !S or !D) ")
                            GameRR[y].append("response")
            except:
                await ctx.send("Please use !RRgame to start the game")

    @commands.command()
    async def D(self,ctx):
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
                            time.sleep(1)
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
    def TimerLeaderboard(self):
        global RrLBoardToggle
        global RRtimer
        while True:
            time.sleep(1)
            RRtimer= RRtimer+1
            if RRtimer>= LeaderboardDelay:
                print("RR leaderboard is useable again")
                RrLBoardToggle= True
                RRtimer= 0
                break

    RRLBcontinue= False
    LeaderboardListRR= []
    @commands.command()
    async def RRleaderboard(self,ctx):
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
            RRtimethread = threading.Thread(target=TimerLeaderboard, args=(self))
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
            RRlboardthread = threading.Thread(target=checkRRfiles, args=(self,ctx))
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

    def checkRRfiles(self,ctx):
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



    @commands.command()
    async def QuitRR(self,ctx):
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
                            currenttime= str(time.strftime("%Y-%m-%D %H:%M:%S", time.localtime()))
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
    def insertion_sort_2d_Descending(self,arr, col_index):
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

async def setup(bot):
      await bot.add_cog(rr(bot))