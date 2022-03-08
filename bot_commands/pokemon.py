# all bot commands related to pokemon
import discord
from discord.ext import commands
from bot_commands.interaction import Interaction as inter
import os, sys
import io
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from lead import Player
import random

class Pokemon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def start(self, ctx):
        player = Player(ctx.author.id)
        if player.user is not None:
            return await ctx.send("You have already chosen a Pokémon!")

        choices = discord.Embed(
            title = 'Welcome to the world of Pokémon!',
            description = 'Please choose one of the following Pokémon with the `p.choose` command',
            color = discord.Color.red()
        )
        bulba1 = '<a:bulba:864332283220328479>'
        bulba2 = '<a:bulbani:864332283288223795>'
        choices.add_field(name = bulba1, value = f"Bulbasaur {bulba2}")
        await ctx.send(embed = choices)
        
    @commands.command(aliases = ["ichooseyou!"])
    async def choose(self, ctx, choice):
        player = Player(ctx.author.id)
        if player.user is not None:
            return await ctx.send("You have already chosen a Pokémon!")
        creationStatus, pokemon = await player.createUser(choice) 
        if creationStatus:
            return await ctx.send(f"Congratulations! You have received a {pokemon}!")
        else:
            return await ctx.send(f"Please choose a valid Pokémon!")

    @commands.command(aliases = ["summary", 'i', 's'])
    async def info(self, ctx):
        player = Player(ctx.author.id)
        user = player.user
        
        if user is None:
            return await player.newUser(ctx)

        status = player.status        

        summary = discord.Embed(
            title = status["name"],
            color = discord.Color.dark_teal()
        )

        cap = status['XPCaps'][status['level']]
        exp = f"{int(status['XP'])}/{int(cap)} EXP Points"

        percent = status['XP'] / cap
        barLen = 12
        filled = int(percent * barLen)
        bar = ('█' * filled) + ('░' * (barLen-filled)) + f' {int(percent*100)}%'

        exp = exp + '\n' + bar

        summary.add_field(name = f'Level: {status["level"]}', value = exp)
        

        meters = status['meters']
        bellyPercent = meters['hunger']['level'] / 255
        bellyFilled = int(bellyPercent * barLen)

        cleanPercent = meters['clean']['level'] / 255
        cleanFilled = int(cleanPercent * barLen)

        affecPercent = meters['affection']['level'] / 255
        affecFilled = int(affecPercent * barLen)

        friendPercent = meters['friendship'] / 255
        friendFilled = int(friendPercent * barLen)

        summary.add_field(name = "Belly", value = ('█' * bellyFilled) + ('░' * (barLen-bellyFilled)) + f' {int(bellyPercent*100)}%', inline = False)
        summary.add_field(name = "Clean", value = ('█' * cleanFilled) + ('░' * (barLen-cleanFilled)) + f' {int(cleanPercent*100)}%', inline = False)
        summary.add_field(name = "Affection", value = ('█' * affecFilled) + ('░' * (barLen-affecFilled)) + f' {int(affecPercent*100)}%', inline = False)
        summary.add_field(name = "Friendship", value = ('█' * friendFilled) + ('░' * (barLen-friendFilled)) + f' {int(friendPercent*100)}%', inline = False)

        img = f'{status.get("name").casefold().capitalize()}.gif'    
        binary = status.get("sprite")
        image = io.BytesIO(binary)
        f = discord.File(image, filename = img)
        summary.set_thumbnail(url = f"attachment://{img}")

        await ctx.send(file = f, embed = summary)


    @commands.command(aliases = ['f', 'b', 'belly', 'eat', 'e'])
    async def feed(self, ctx):
        user = Player(ctx.author.id)
        food = ["Apple", "Banana", "Plain Bean", "Basic Poké Puff", "Curry", "Pokéblock", "Poffin", "Rage Candy Bar", "Lava Cookie", "Old Gateau", "Casteliacone", "Lumiose Galette", "Shalour Sable", "Big Malasada", "Gummi", "Berry"]
        feedStatus = await inter.feed(user)
        msg = f"You fed your {user.status.get('name')} 1 {random.choice(food)}!" if feedStatus else f"{user.status.get('name')} is full! It can't take another bite!"
        await ctx.send(msg)

    @commands.command(aliases = ['pc', 'p'])
    async def pokemon(self, ctx):
        return 1

    @commands.command(aliases = ['lm'])
    async def levelMessage(self, ctx, message):
        #### INCOMPLETE ####
        user = Player(ctx.author.id)
        if str(message) == 'default':
            return user.setLevelMessage(user.levelDefault)
        return user.setLevelMessage(message)

def setup(bot):
    bot.add_cog(Pokemon(bot))