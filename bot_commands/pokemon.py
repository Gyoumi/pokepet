# all bot commands related to pokemon
import discord
from discord.ext import commands
import os, sys
import io
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from lead import Player

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

        cap = status['XPCaps'][status['Level']]
        exp = f"{int(status['XP'])}/{int(cap)} EXP Points"

        percent = status['XP'] / cap
        barLen = 12
        filled = int(percent * barLen)
        bar = ('█' * filled) + ('░' * (barLen-filled)) + f' {int(percent*100)}%'

        exp = exp + '\n' + bar

        summary.add_field(name = f'Level: {status["Level"]}', value = exp)
        summary.add_field(name = "Stomach", value = '░' * barLen, inline = False)
        summary.add_field(name = "Clean", value = '░' * barLen, inline = False)
        summary.add_field(name = "Affinity", value = '░' * barLen, inline = False)
        summary.add_field(name = "Friendship", value = '░' * barLen, inline = False)

        img = f'{status.get("name").casefold().capitalize()}.gif'    
        binary = status.get("sprite")
        image = io.BytesIO(binary)
        f = discord.File(image, filename = img)
        summary.set_thumbnail(url = f"attachment://{img}")

        await ctx.send(file = f, embed = summary)

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