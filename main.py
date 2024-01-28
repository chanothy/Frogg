from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
from discord.ext import commands
from music_cog import music_cog
from help_cog import help_cog

# load token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# # bot setup
intents: Intents = Intents.default()
intents.message_content = True 
client: Client = Client(intents=intents)

# # message funciton
# async def send_message(message: Message, user_message: str) -> None:
#     if not user_message:
#         print("Message was empty")
#         return
    
#     if is_private := user_message[0] == '?':
#         user_message = user_message[1:]
    
#     try: 
#         response: str = get_response(user_message)
#         await message.author.send(response) if is_private else await message.channel.send(response)
#     except Exception as e:
#         print(e)

# # startup
# @client.event
# async def on_ready():
#     print(f'{client.user} is now froggy.')

# # incoming messages
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     username = str(message.author)
#     user_message = message.content
#     channel = str(message.channel)

#     print(f'[{channel}] {username}: "{user_message}"')

#     await send_message(message, user_message)

# music function
def musicStart():
    bot = commands.Bot(command_prefix="/",intents=intents)
    bot.add_cog(music_cog(bot))
    bot.add_cog(help_cog(bot))
    bot.remove_command("help")
    bot.run(token=TOKEN)


# entry
def main():
    musicStart()

if __name__ == '__main__':
    main()