import discord
from discord.ext import commands
from .commands import Dictionary, EasterEggs, Spotify

from .lyrics.sources.genius import GeniusSource
from lyricsgenius import Genius

token = "Njk5NDUzOTAwMTI1NjM0NjUw.XpUnSA.nw-SkhhMU624YQ-sucF5-HT5Lxc"
genius_token = "1_zoI40CenkBNdmACg0zNc13HIjJyBGcRKp0D2d6EYeHqMP0unsJb7qDq9tMHAmN"

bot = commands.Bot(command_prefix="!")

bot.add_cog(Dictionary(bot))
bot.add_cog(EasterEggs(bot))
bot.add_cog(Spotify(bot, GeniusSource(Genius(genius_token))))

bot.run(token)