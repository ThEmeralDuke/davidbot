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
import json
import random
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

# Load settings from the JSON file
with open("config.json", "r") as f:
    SETTINGS = json.load(f)

def cog_is_active():
    async def predicate(ctx):
        server_id = str(ctx.guild.id)
        cog_name = ctx.cog.__class__.__name__.lower()  # Get current cog's name in lowercase

        server_data = SETTINGS.get(server_id)
        if not server_data:
            return False
        active_cogs = server_data.get("CogsActive", [])
        return cog_name in active_cogs
    return commands.check(predicate)

class gambling(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
        self.money =0
        self.symbolarray = [
        [":cherries:", ":lemon:", ":tangerine:", ":pear:", ":melon:", ":grapes:"],  # Common
        [":tickets:", ":bell:"],  # Uncommon
        [":moneybag:"]  # Rare (Jackpot)
        ]
        self.slotweight= [0.75,0.175,0.075]
        self.SlotRings= [[],[],[]]

    @commands.Cog.listener()
    async def on_ready(self):
         print("gambling.py is ready")

    @commands.command()
    @cog_is_active()
    async def Slots(self, ctx, money=None):
        try:
            money = float(money)
            self.money = money
            for ring in range(3):
                print(ring)
                list= random.choices(
                self.symbolarray, self.slotweight, k=3)
                for iteration in list:
                    lengthOfIteration = random.randint(0,(len(iteration)-1))
                    self.SlotRings[ring].append(iteration[lengthOfIteration])
                    
            await ctx.send(self.SlotRings[0][0]+self.SlotRings[1][0]+self.SlotRings[2][0])
            await ctx.send(self.SlotRings[0][1]+self.SlotRings[1][1]+self.SlotRings[2][1])
            await ctx.send(self.SlotRings[0][2]+self.SlotRings[1][2]+self.SlotRings[2][2])
            self.SlotRings= [[],[],[]]
        except:
            await ctx.send("Please input a valid number to bet with")


async def setup(bot):
      await bot.add_cog(gambling(bot))