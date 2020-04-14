from discord.ext import commands
from .dictionary.models.word import Reading
from .dictionary.sources.common import Source
from .dictionary.sources.jisho import JishoSource

class Dictionary(commands.Cog):
    MAX_RESULTS = 3
    def __init__(self, bot, source: Source = JishoSource()):
        self.bot = bot
        self.source: Source = source
    
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
