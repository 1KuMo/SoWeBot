# SoWeBot 𐔌՞. .՞𐦯
*(Work in Progress — V1 Modular & Discord Integration)*

**SoWeBot** is an automated pipeline and tool designed to interface with the SoWeSign student portal, ensuring students never miss an attendance check-in (Elearning, remote courses, etc.) by handling session authentication, real-time course timing checks, and broadcasting reminders directly to a Discord server.

---

> **Important Note:** **SoWeBot** does **not** automatically sign or check you in on the school portal. Its sole purpose is to act a smart reminder system, notifying you on Discord the exact moment an attendance window opens so you never forget to sign manually.
> *Want access to the notification server? Feel free to contact me on Discord! n3li0*

---

## Overview

Managing attendance on school portals can be tedious, especially when session tokens expire or unexpected schedule changes happen. **SoWeBot** automates the heavy lifting:
1. **Smart Authentication & Auto-Refresh:** Automatically handles SoWeSign Access Tokens and uses Refresh Tokens stored securely in `.env` to silently renew sessions when an expiration occurs (`400`/`401` error trapping with dynamic `.env` updates).
2. **Real-time Schedule Fetching:** Pulls future courses directly from the SoWeSign student portal API dynamically.
3. **Filtering & Categorization:** Isolates target course types (Elearning, Conferences, etc.) and isolates today's active schedule.
4. **Precision Timing:** Computes exact opening and closing windows for attendance checking based on course offsets (`openingDelay` and `closingDelay`).
5. **Discord Notifications:** Runs asynchronously via a secondary local Arch Linux machine to alert students in real time.

---

## Tech Stack & Architecture

- **Language:** Python 3.10+
- **Bot Framework:** `discord.py` (Asynchronous event loops & background tasks)
- **HTTP Requests:** `requests`
- **Environment Management:** `python-dotenv` (`load_dotenv`, `set_key`)
- **Time & Date Management:** Native Python `datetime`, `date`, `timedelta`
- **Environment:** Linux (Optimized and tested on Arch Linux)

---

## Project Structure

```text
SOWEBOT/
├── discord_bot/
│   └── main.py            # Discord bot wrapper & background task loops
├── sowebot/
│   ├── main.py            # Core engine, API calls, auto-refresh, and time-window logic
│   └── help.md            # Technical documentation & data structures
├── .env                   # Environment variables (SWS_KEY, REFRESH_TOKEN, BOT_TOKEN, DISCORD_CHANNEL_ID) — keep it private
└── README.md
```

---

## Setup

### 1. Clone and create the two environments

```bash
git clone https://github.com/1KuMo/SoWeBot.git
cd SoWeBot

python3 -m venv sowebot/.venv
sowebot/.venv/bin/pip install requests python-dotenv

python3 -m venv discord_bot/.venv
discord_bot/.venv/bin/pip install discord.py python-dotenv
```

The bot calls `sowebot/.venv/bin/python` directly, so keep this folder layout as-is.

### 2. Configure `.env`

Create a `.env` file at the repo root with:

```text
SWS_KEY=<SoWeSign access token>
REFRESH_TOKEN=<SoWeSign refresh token>
BOT_TOKEN=<Discord bot token>
DISCORD_CHANNEL_ID=<numeric channel ID>
```

- `BOT_TOKEN` comes from the Discord Developer Portal.
- `DISCORD_CHANNEL_ID` is a number: enable Developer Mode in Discord, then right-click the channel and copy its ID.
- The SoWeSign tokens come from a logged-in session; `sowebot/help.md` documents the refresh endpoint.
- Never commit this file.

### 3. Discord permissions

Invite the bot to your server and give it permission to send messages in the target channel.

### 4. Run it

```bash
discord_bot/.venv/bin/python discord_bot/main.py
```

The bot logs in, then scans once a minute. One reminder is sent per course occurrence and the deduplication list resets each day.

To check the scanner on its own:

```bash
sowebot/.venv/bin/python sowebot/main.py
```

It prints the active courses as JSON on stdout; debug output goes to stderr.

### 5. Two things to keep in mind

- The machine should use the same timezone as the portal: course times are compared as local naive datetimes.
- `REFRESH_TOKEN` expires after about a month. Renew it manually when the refresh starts failing.

---

> **Note:** I used AI to help structure and complete this documentation to make it as thorough and clear as possible, + the discord bot is mostly ( absolutely ) vibe-coded since I can't deal with discord bots idk why.  Contributions and feedback are warmly welcomed!

```text
 /\_/\  
( o.o ) 
 > ^ <  
           ____  __    __   ____
          (_  _)/  \  / _\ (    \
            )( (  O )/    \ ) D (
           (__) \__/ \_/\_/(____/
```
