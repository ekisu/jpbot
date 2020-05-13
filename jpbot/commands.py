from typing import Optional, Tuple

import discord
from discord.ext import commands

from .dictionary.models.word import Reading
from .dictionary.sources.common import Source as DictionarySource
from .dictionary.sources.jisho import JishoSource

from .lyrics.sources.common import Source as LyricsSource

class Dictionary(commands.Cog):
    MAX_RESULTS = 3
    def __init__(self, bot, source: DictionarySource = JishoSource()):
        self.bot = bot
        self.source: DictionarySource = source
    
    @commands.command()
    async def word(self, ctx, *, term):
        def reading_to_string(r: Reading) -> str:
            parts = filter(None, [r.word, r.reading])
            return "/".join(parts)
                
        results = self.source.search_for_word(term)

        text = ""
        text += f"Found {len(results)} word{'s' if len(results) != 1 else ''}.\n\n"

        for word in results[:self.MAX_RESULTS]:
            readings = word.readings
            senses = word.senses

            text += reading_to_string(readings[0])
            if len(readings) > 1:
                additional_readings_strings = [
                    reading_to_string(additional_reading)
                    for additional_reading in readings[1:]
                ]

                text += f" (also {', '.join(additional_readings_strings)})"
            
            text += "\n\n"
            
            for index, sense in enumerate(senses):
                text += f"{index + 1}. {', '.join(sense.definitions)}.\n"
            
            text += "\n"
        
        await ctx.send(text) 

class EasterEggs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.apply_decorators()
    
    def apply_decorators(self):
        @self.bot.event
        async def on_message(message: discord.Message):
            if message.content.lower() in ["chama fiote", "chama fiote."]:
                await message.channel.send("chama.")
                return
            
            if self.bot.user in message.mentions:
                yoroshiku_messages = [
                    "よろしくおねがい",
                    "よろしくお願い"
                ]

                if any(msg in message.content for msg in yoroshiku_messages):
                    await message.channel.send("こちらこそ！")
                else:
                    await message.channel.send("よろしくおねがいします！")
                
                return
            
            await self.bot.process_commands(message)

class Spotify(commands.Cog):
    def __init__(self, bot: commands.Bot, lyrics_source: LyricsSource):
        self.bot: commands.Bot = bot
        self.lyrics_source = lyrics_source
    
    def _find_member_currently_playing_song(self, member: discord.Member) -> Optional[Tuple[str, str]]:
        for activity in member.activities:
            if activity.name == "Spotify":
                return (activity.artist, activity.title)
        
        return None

    @commands.command()
    async def nplyrics(self, ctx):
        currently_playing = self._find_member_currently_playing_song(ctx.author)

        if currently_playing is None:
            await ctx.send("Nothing is being played right now!")
            return
        
        artist, title = currently_playing

        song = self.lyrics_source.search_for_artist_and_title(artist, title)

        text = f"Currently playing {title} by {artist}!\n\n"
        if song is not None:
            text += "Lyrics:\n"
            text += song.lyrics.lyrics
        else:
            text += "Lyrics couldn't be found."

        await ctx.send(text)
        