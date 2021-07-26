#commands and other discord stuff related to the user themself
from discord.ext import commands
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.user)

    def getCooldown(self, message):
        bucket = self._cd.get_bucket(message)
        return bucket.update_rate_limit()

def setup(bot):
    bot.add_cog(User(bot))