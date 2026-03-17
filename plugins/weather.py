import asyncio
import random
import requests
from bs4 import BeautifulSoup
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

# --- CONFIG ---
AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"

def get_remote_aura():
    try:
        response = requests.get(AURA_URL, timeout=5)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except Exception:
        pass
    return ["**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤𝖣** 🛡️"]

# ================= WEATHER CMD (NO KEY - DIRECT) =================
@events.register(events.NewMessage(pattern=r"\.weather ?(.*)"))
async def weather_search(event):
    client = event.client

    # 🛡️ 1. NO ENTRY LOGIC (For unknown users in PM)
    if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        aura_list = get_remote_aura()
        selected_aura = random.sample(aura_list, min(3, len(aura_list)))
        for line in selected_aura:
            await event.edit(line)
            await asyncio.sleep(1.5) # Forceful 5s approx delay
        return

    # 🛠️ 2. BAN & MAINTENANCE & SUDO CHECK
    if await is_banned(event.sender_id):
        return
    if await get_maintenance() and event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
        return await event.edit("`System Status: Maintenance Mode.`")

    place = event.pattern_match.group(1).strip()
    if not place:
        return await event.edit("`Error: City name ya Pincode toh do?`")

    await event.edit(f"`☁️ Scanning Atmosphere: {place}...`")

    try:
        # 🚀 SAKTI LOGIC: Google Weather Scraping (No API Key needed)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        search_query = f"weather in {place}"
        res = requests.get(f"https://www.google.com/search?q={search_query.replace(' ', '+')}&hl=en", headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Data Extraction
        location = soup.find("div", attrs={'id': 'wob_loc'}).get_text()
        temp = soup.find("span", attrs={'id': 'wob_tm'}).get_text()
        condition = soup.find("span", attrs={'id': 'wob_dc'}).get_text()
        humidity = soup.find("span", attrs={'id': 'wob_hm'}).get_text()
        wind = soup.find("span", attrs={'id': 'wob_ws'}).get_text()

        # 📋 Point-to-Point Clean Result (3-4 Chhoti Lines)
        weather_res = (
            f"📍 **Location:** `{location}`\n"
            f"🌡️ **Temp:** `{temp}°C` | `{condition}`\n"
            f"💧 **Humidity:** `{humidity}`\n"
            f"💨 **Wind Speed:** `{wind}`\n\n"
            f"**DARK-USERBOT** 💀"
        )
        await event.edit(weather_res)

    except Exception:
        # Fallback agar Google Scraping fail ho (rare case)
        await event.edit("`❌ Error: Location not found or server busy.`")


# ================= SETUP =================
async def setup(client):
    client.add_event_handler(weather_search)
      
