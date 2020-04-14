import discord
from discord.ext import commands
from .commands import Dictionary

token = "Njk5NDUzOTAwMTI1NjM0NjUw.XpUnSA.nw-SkhhMU624YQ-sucF5-HT5Lxc"

bot = commands.Bot(command_prefix="!")
bot.add_cog(Dictionary(bot))

bot.run(token)