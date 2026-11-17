import discord
from dotenv import find_dotenv, load_dotenv
import os

env_file = find_dotenv()
load_dotenv(env_file)

if not os.getenv("BOT_TOKEN"):
    raise ValueError("bot token needed")

token = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        
client.run(token)
