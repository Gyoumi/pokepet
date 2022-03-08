from lead import Player
from discord.ext import tasks, commands
import datetime
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
class Interaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.meterCheck.start()

    @tasks.loop(seconds=5)
    async def meterCheck(self):
        print("checking meters...")
        try:
            data = Player.getAllUsers()
            self.currTime = datetime.datetime.now()
            for user in data:
                meters = user.get("Pokemon").get("meters")
                await self.dropHunger(user.get('_id'), meters)
                await self.dropClean(user.get('_id'), meters)
                await self.dropAffection(user.get('_id'), meters)
        except Exception as e:
            print("error updating meter due to", e)

    async def dropHunger(self, id, meter):
        await self.dropLevels(id, 'hunger', meter, 10)            

    async def dropClean(self, id, meter):
        await self.dropLevels(id, 'clean', meter, 15)
    
    async def dropAffection(self, id, meter):
        await self.dropLevels(id, 'affection', meter, 30)

    async def dropLevels(self, id, name, meter, duration):
        type = meter.get(name)
        level = type.get("level")
        time = type.get("time")
        if level == 0:
            return
        if time + datetime.timedelta(seconds=duration) <= self.currTime:
            player = Player(id)
            player.updateMeter(name, self.currTime, -3)
            print("updated " + name + "!")

    @classmethod
    async def feed(cls, user):
        cls.currTime = datetime.datetime.now()
        meter = user.status.get("meters")
        hungerLevel = meter.get("hunger").get('level')
        affectionLevel = meter.get("affection").get('level')
        if hungerLevel >= 255:
            return False
        user.updateMeter("hunger", cls.currTime, min(100, 255-hungerLevel))
        if affectionLevel <= 255:
            user.updateMeter("affection", cls.currTime, min(5, 255-affectionLevel))
        return True

    @classmethod
    async def clean(cls, user):
        

def setup(bot):
    bot.add_cog(Interaction(bot))