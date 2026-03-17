import asyncio
import random
import requests
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

# ================= WEATHER CMD =================
@events.register(events.NewMessage(pattern=r"\.weather ?(.*)"))
async def weather_search(event):
    client = event.client

    # 🛡️ 1. NO ENTRY LOGIC
    if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        aura_list = get_remote_aura()
        selected_aura = random.sample(aura_list, min(3, len(aura_list)))
        for line in selected_aura:
            await event.edit(line)
            await asyncio.sleep(1.5) 
        return

    # 🛠️ 2. SECURITY CHECKS
    if await is_banned(event.sender_id):
        return
    if await get_maintenance() and event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
        return await event.edit("`System Status: Maintenance Mode Active.`")

    place = event.pattern_match.group(1).strip()
    if not place:
        return await event.edit("`Error: City name or Pincode required!`")

    await event.edit(f"`☁️ Scanning Atmosphere: {place}...`")

    # 🚀 3. WTTR LOGIC WITH RETRY
    max_retries = 2
    for attempt in range(max_retries):
        try:
            # Format: Location, Temp+Condition, Wind, Humidity
            url = f"https://wttr.in/{place}?format=%l\n🌡️+%t+%C\n💨+Wind:+%w\n💧+Hum:+%h"
            res = requests.get(url, timeout=8).text

            if "Unknown location" in res or "404" in res:
                return await event.edit("`❌ Error: Location not found!`")

            # Point-to-Point Clean Result
            weather_res = (
                f"☁️ **Weather Report**\n"
                f"────────────────\n"
                f"`{res}`\n"
                f"────────────────\n"
                f"💀 **DARK-USERBOT**"
            )
            return await event.edit(weather_res)

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            if attempt < max_retries - 1:
                await event.edit(f"`⏳ Server busy, Retrying... ({attempt + 1})`")
                await asyncio.sleep(2)
                continue
            else:
                return await event.edit("`❌ Error: WTTR server busy. Try again later.`")

# ================= SETUP =================
async def setup(client):
    client.add_event_handler(weather_search)
        
