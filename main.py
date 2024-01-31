from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
from discord.ext import commands
# from music_cog import music_cog
# from help_cog import help_cog

# load token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# # bot setup
intents: Intents = Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix="/",intents=intents)

# startup
@bot.event
async def on_ready():
    print(f'{bot.user} is now froggy.')
    
@bot.command(name='foo')
async def foo(ctx, arg):
    await ctx.send(arg)

# entry
def main():
    bot.run(token = TOKEN)


if __name__ == '__main__':
    main()