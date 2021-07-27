# deals with database stuff with MongoDB
from pymongo import MongoClient
import client as pAPI
import requests
import util
import os
import datetime

class Player:
    #each Pokemon has characteristics in following format:
    #   _id, level, XP, XPCaps, sprite, {meters}
    # meters {hunger, clean, affection, friendship}

    url = os.environ.get("MON_CLUSTER1")
    cluster = MongoClient(url)
    db = cluster['Database0']
    collection = db["Collection0"]

    def __init__(self, id):
        self.id = id
        self.user = self.getUser()
        if self.user is not None:
            self.status = self.user["Pokemon"]

    async def newUser(self, ctx):
        await ctx.channel.send("Please use the `p.start` command to pick your first Pokémon!")
        
    async def createUser(self, starterName):
        try:    # first checking if user input a Pokedex number instead of a name
            id = int(starterName)
            name, mon = pAPI.findPokemon(id)
        except (ValueError, requests.exceptions.HTTPError) as exception:
            print(f'Caught error in createUser() method: {exception}')
            name, mon = pAPI.findPokemon(starterName.casefold())
        if mon is None:     # invalid dex number and/or name
            return False, mon
        
        growth = pAPI.getExpRate(mon)
        growth.append(0)    #just to make the array size 101 :)

        binary = pAPI.getPokemonSpriteBytes(name)   #bytes for sprite gif

        friendship = pAPI.getBaseFriendship(mon)
        currTime = datetime.datetime.now()
        meters = {"hunger": {"level":255, "time": currTime}, "clean": {"level": 64, "time": currTime}, "affection": {"level": 0, "time": currTime}, "friendship": friendship}
        
        starter = {"name": name, "level": 5, "XP": 0, "XPCaps": growth, "sprite": binary, "meters": meters}
        self.updateDB({"_id": self.id, "Pokemon": starter})
        return True, starter["name"]
        
    def updateDB(self, data):
        self.collection.insert_one(data)

    def getUser(self):
        return self.collection.find_one({'_id': self.id})       

    async def expGain(self, message):
        current = self.status
        if current['level'] == 100:
            return
        level = current['level']
        old = current["XP"]
        cap = current['XPCaps'][level]
        b, enemy = util.binarySearchExpGain(level)
        enemy = min(max(1, level + enemy), 100)
        gain = (old + int((b * enemy / 5) * (((2 * enemy + 10) / (enemy + level + 10))**2.5)))
        print(gain - old, gain, cap)
        remaining = max(cap - gain, cap)
        growth = 0
        while cap < gain:
            gain -= remaining
            growth += 1
            cap = current['XPCaps'][level+growth]
            remaining = max(cap - gain, cap)

        update = {'$set':{'Pokemon.XP': gain}}

        if growth > 0:
            #level up
            update['$inc'] = {
                'Pokemon.level': growth,
                }
            await message.channel.send(self.levelDefault(growth))
        self.updateUser(update)

    def updateUser(self, details):
        self.collection.update(self.user, details)
        self.user = self.getUser()

    def levelDefault(self, growth):
        return f'__**Congratulations!**__ Your {self.status.get("name")} has reached level {self.status.get("level")+growth}!'

    def levelUpMessage(self):
        if self.user.get('levelMessage') is not None:
            return self.user['levelMessage']
        self.setLevelMessage(self.levelDefault())
        return self.levelDefault()

    def setLevelMessage(self, message):
        self.updateUser({
            '$set': {
                'levelMessage': message
            }
        })

    def getMeters(self):
        return self.status.get("meters")

    def updateMeter(self, meter, time, amount):
        update = {
            '$set': { 
                f'Pokemon.meters.{meter}.time': time
                }
            }
        update['$inc'] = {
            f'Pokemon.meters.{meter}.level': amount
        }
        self.updateUser(update)

    @classmethod
    def getAllUsers(cls):
        return cls.collection.find({})