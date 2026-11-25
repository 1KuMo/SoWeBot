import asyncio
import json
import logging
import os
import subprocess
from datetime import date, datetime
from pathlib import Path

import discord
from discord.ext import tasks
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"
SOWEBOT_DIR = BASE_DIR / "sowebot"
SOWEBOT_PYTHON = SOWEBOT_DIR / ".venv" / "bin" / "python"
SOWEBOT_SCRIPT = SOWEBOT_DIR / "main.py"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("sowebot")
logging.getLogger("discord").setLevel(logging.WARNING)

load_dotenv(ENV_FILE)

if not os.getenv("BOT_TOKEN"):
    raise ValueError("bot token needed")
if not os.getenv("DISCORD_CHANNEL_ID"):
    raise ValueError("DISCORD_CHANNEL_ID needed")

BOT_TOKEN = os.getenv("BOT_TOKEN")

try:
    CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
except ValueError as exc:
    raise ValueError("DISCORD_CHANNEL_ID must be an integer") from exc

if not SOWEBOT_PYTHON.is_file():
    raise FileNotFoundError(f"sowebot interpreter not found: {SOWEBOT_PYTHON}")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

_notified = set()
_notified_day = None


def get_active_courses():
    result = subprocess.run(
        [str(SOWEBOT_PYTHON), str(SOWEBOT_SCRIPT)],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        timeout=60,
        check=True,
    )
    courses = json.loads(result.stdout)
    if not isinstance(courses, list):
        raise ValueError(f"unexpected sowebot output: {result.stdout[:200]!r}")
    return courses


def build_embed(cours):
    debut = datetime.fromisoformat(cours["debut"])
    fin = datetime.fromisoformat(cours["fin"])
    embed = discord.Embed(
        title=f"⏰ {cours['nom']}",
        description=f"Fenêtre de pointage ouverte — `{cours['categorie']}`",
        color=discord.Color.gold(),
        timestamp=datetime.now().astimezone(),
    )
    embed.add_field(name="Début", value=debut.strftime("%H:%M"), inline=True)
    embed.add_field(name="Fin", value=fin.strftime("%H:%M"), inline=True)
    embed.add_field(name="Fenêtre", value=f"-{cours['opening']} / +{cours['closing']}", inline=True)
    return embed


async def get_channel():
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        channel = await client.fetch_channel(CHANNEL_ID)
    return channel


@client.event
async def on_ready():
    logger.info("Logged in as %s", client.user)
    if not scan_check.is_running():
        scan_check.start()


@tasks.loop(minutes=1)
async def scan_check():
    global _notified_day

    today = date.today().isoformat()
    if today != _notified_day:
        _notified.clear()
        _notified_day = today

    channel = await get_channel()
    courses = await asyncio.to_thread(get_active_courses)

    for cours in courses:
        key = (cours.get("id"), cours.get("debut"))
        if key in _notified:
            continue
        await channel.send(embed=build_embed(cours))
        _notified.add(key)


@scan_check.before_loop
async def before_scan_check():
    await client.wait_until_ready()


@scan_check.error
async def on_scan_error(error):
    logger.error("scan_check failed", exc_info=(type(error), error, error.__traceback__))


if __name__ == "__main__":
    client.run(BOT_TOKEN)
