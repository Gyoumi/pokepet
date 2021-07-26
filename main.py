import discord
from discord.ext import commands
import os
from lead import Player

bot = commands.Bot(command_prefix='p.', case_insensitive=True)

for file in os.listdir('./bot_commands'):
    if file.endswith('.py'):
        bot.load_extension(f'bot_commands.{file[:-3]}')

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    print('Ready!')
    return await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name= 'Pokémon Journeys'))

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.event
async def on_message(message):
    user = bot.get_cog('User')
    cooldown = user.getCooldown(message)
    if message.author != bot.user and not message.author.bot:
        if cooldown is None:
            #add exp to user
            player = Player(message.author.id)
            if player.user is not None:
                await player.expGain(message)
        else:
            print('user cooldown activated', cooldown)

    if str(message.content)[:2].casefold() == 'p.':
        #bot command
        return await bot.process_commands(message)

bot.run(os.environ.get("MON_TOKEN"))