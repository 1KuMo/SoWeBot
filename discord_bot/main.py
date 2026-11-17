import discord
from discord.ext import tasks
from dotenv import find_dotenv, load_dotenv
import os

env_file = find_dotenv()
load_dotenv(env_file)

if not os.getenv("BOT_TOKEN"):
    raise ValueError("bot token needed")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

token = os.getenv("BOT_TOKEN")
channel_id = int(os.getenv("DISCORD_CHANNEL_ID"))

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(channel_id)
    scan_check.start(channel)
    await channel.send('hello')


@tasks.loop(minutes=5)
async def scan_check(channel):
    await channel.send("Hello world!", get_active_courses())
    
client.run(token)
