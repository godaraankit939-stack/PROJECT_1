import asyncio
import random
import requests
from datetime import datetime
from telethon import events, functions, types
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import InputStickerSetShortName
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

# --- GITHUB CONFIG (Aura Lines) ---
AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"

def get_remote_aura():
    try:
        response = requests.get(AURA_URL, timeout=5)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except:
        pass
    return ["**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤𝖣** 🛡️"]

def get_account_age(user_id):
    if user_id < 100000000: return "10+ Years (Ancient)"
    if user_id < 500000000: return "7-9 Years"
    if user_id < 1000000000: return "5-6 Years"
    if user_id < 2000000000: return "2-3 Years"
    if user_id < 5000000000: return "1-2 Years"
    return "New Account (Less than 1 Year)"

@events.register(events.NewMessage(pattern=r"\.info ?(.*)"))
async def user_info(event):
    client = event.client
    me = await client.get_me()

    # 🛡️ 1. NO ENTRY LOGIC
    if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        aura_list = get_remote_aura()
        for line in random.sample(aura_list, min(3, len(aura_list))):
            await event.edit(line)
            await asyncio.sleep(1.5)
        return

    # 🛠️ 2. BAN & MAINTENANCE CHECK
    if await is_banned(event.sender_id): return
    if await get_maintenance() and event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
        return await event.edit("`Status: Maintenance Mode Active.`")

    input_str = event.pattern_match.group(1).strip()
    reply = await event.get_reply_message()
    
    await event.edit("`🔍 Scanning User Intelligence...`")

    try:
        if reply:
            user = await client.get_entity(reply.sender_id)
        elif input_str:
            user = await client.get_entity(input_str)
        else:
            user = me

        full_user = await client(GetFullUserRequest(user.id))
        
        # Core Details
        u_id = user.id
        first_name = user.first_name
        last_name = user.last_name or ""
        username = f"@{user.username}" if user.username else "None"
        dc_id = user.photo.dc_id if user.photo else "Unknown"
        bio = full_user.full_user.about or "No Bio Provided"
        common_chats = full_user.full_user.common_chats_count
        
        # History & Age
        acc_age = get_account_age(u_id)
        
        # Sticker Intelligence (Checks for User's Profile Stickers/Packs)
        sticker_info = "No Public Sticker Packs Found"
        if hasattr(full_user.full_user, 'profile_stickers') and full_user.full_user.profile_stickers:
            sticker_info = "Custom Profile Stickers Active"

        # Constructing Report
        info_msg = (
            f"👤 **USER INTELLIGENCE REPORT**\n\n"
            f"◈ **Full Name:** `{first_name} {last_name}`\n"
            f"◈ **User ID:** `{u_id}`\n"
            f"◈ **Username:** {username}\n"
            f"◈ **Data Center:** `DC-{dc_id}`\n"
            f"◈ **Account Age:** `{acc_age}`\n\n"
            f"◈ **Common Groups:** `{common_chats}`\n"
            f"◈ **Stickers:** `{sticker_info}`\n\n"
            f"◈ **Bio:** `{bio}`\n\n"
            f"**Powered By DARK-USERBOT** 💀"
        )
        
        await event.edit(info_msg)

    except Exception as e:
        await event.edit(f"❌ **Intelligence Failure:** `{str(e)}`")

# --- SETUP FUNCTION ---
async def setup(client):
    client.add_event_handler(user_info)
  
