#Loading Log files
filepath= "."
Errorlog= filepath+"/ImportantTxtFiles/Logs/Error.log"
def LogError(Level,Reason):
    with open (Errorlog, "a") as log:
            currenttime= str(time.strftime("%Y-%m-%D %H:%M:%S", time.localtime()))
            log.write(f"{currenttime}    ({Level}) {Reason}\n")
    log.close()


#loading libraries
from dotenv import *
import discord
from discord import *
from discord.ext import commands
from discord.utils import *
import time
import csv

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


class gambling(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
        self.money =0
        self.symbolarray= [":cherries:",":lemon:",":orange:",":pear:",":melon:",":grapes:"]
        self.symbols = " ".join(self.symbolarray)
        self.ringone= []
        self.ringtwo= []
        self.ringthree= []

    @commands.Cog.listener()
    async def on_ready(self):
         print("gambling.py is ready")

    @commands.command()
    async def Slots(self, ctx, money=None):
        try:
            money = float(money)
            self.money = money
            
            await ctx.send(self.symbols)
            
        except:
            await ctx.send("Please input a valid number to bet with")


async def setup(bot):
      await bot.add_cog(gambling(bot))