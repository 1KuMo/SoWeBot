# SoWeBot 𐔌՞. .՞𐦯
*(Work in Progress — V1 Core Engine Functional)*

**SoWeBot** is an automated pipeline and tool designed to interface with the SoWeSign student portal, ensuring students never miss an attendance check-in (Elearning, remote courses, etc.) by handling session authentication and real-time course timing checks automatically.

---

## 🌟 Overview

Managing attendance on school portals can be tedious, especially when session tokens expire or unexpected schedule changes happen. **SoWeBot** automates the heavy lifting:
1. **Smart Authentication & Auto-Refresh:** Automatically handles SoWeSign Access Tokens and uses Refresh Tokens stored securely in `.env` to silently renew sessions when an expiration occurs (`400`/`401` error trapping with dynamic `.env` updates).
2. **Real-time Schedule Fetching:** Pulls future courses directly from the SoWeSign student portal API dynamically.
3. **Filtering & Categorization:** Isolates target course types (Elearning, Conferences, etc.) and isolates today's active schedule.
4. **Precision Timing:** Computes exact opening and closing windows for attendance checking based on course offsets (`openingDelay` and `closingDelay`).

---

## 🛠️ Tech Stack & Architecture

- **Language:** Python 3.10+
- **HTTP Requests:** `requests`
- **Environment Management:** `python-dotenv` (`load_dotenv`, `set_key`)
- **Time & Date Management:** Native Python `datetime`, `date`, `timedelta`
- **Environment:** Linux (Optimized and tested on Arch Linux)

---

## 📂 Project Structure

```text
SOWEBOT/
├── venv/                  # Python virtual environment (ignored by git)
├── main.py                # Core engine, authentication flow, and time-window logic
├── .env                   # Environment variables (SWS_KEY, REFRESH_TOKEN) (ignored by git)
└── README.md
```

---
> **Note:** I used AI to help structure and complete this documentation to make it as thorough and clear as possible. Contributions and feedback are warmly welcomed!

```text
 /\_/\  
( o.o ) 
 > ^ <  
            ____  __    __    ____
           (_   _)/  \  / _\ (    \
            )( (   O )/    \ ) D (
           (__) \__/ \_/\_/(____/
```
