import asyncio
import random
import requests
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

# --- CONFIG ---
AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"
# Remote list (Optional for later)
MEME_REPO = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/memes_list.txt"

# 🚀 Curated Meme List (Links for instant working)
STARTER_MEMES = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJndXp4bmZ5Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7bu12GHm4G5FrnOg/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbmZ5Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l1KsBR3ahp30S6OCQ/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKHKjrDyqphX9C0/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKVUn7iM8FMEU24/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKSjPKYM91q8yFq/giphy.gif",
    "https://graph.org/file/f6e245a4993a45c7e3f88.mp4", # Example MP4
    "https://graph.org/file/98e6d987d6e5a6c5b4e3a.mp4",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l0Ex6Ut3wVcHWLT68/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o6wrvPZ3ZPF3n0G2M/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/26gsjCZpPolPr3sBy/giphy.gif",
    "https://graph.org/file/876543210fedcba987654.mp4",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l2YWCHf5RZypvawHm/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l1Ku9u4y5m6iCjSyk/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKMt1VVNkXRYDra/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l41lM8A5pBAH7U5Ww/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o6Zt6ML6BByX6fHJS/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/26vUxJ97iTrpT9s7C/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o6Zt7q6vG6C6uR3m0/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l0Exu3AdO7y992nba/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4Znd4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/26vUAAa0fU79LByC4/giphy.gif"
]

# Anti-Repeat Memory
RECENT_MEMES = []

def get_remote_aura():
    try:
        response = requests.get(AURA_URL, timeout=5)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except: pass
    return ["**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤𝖣** 🛡️"]

# ================= RANDOM MEME LOGIC =================

@events.register(events.NewMessage(pattern=r"\.meme$"))
async def meme_cmd(event):
    # 🛡️ 1. NO ENTRY LOGIC
    if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        aura = get_remote_aura()
        for line in random.sample(aura, 3):
            await event.edit(line)
            await asyncio.sleep(1.5)
        return

    # 🛠️ 2. SECURITY CHECKS
    if await is_banned(event.sender_id): return
    if await get_maintenance() and event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
        return await event.edit("`System Status: Maintenance Mode.`")

    await event.edit("`📦 Opening Meme Pitara...`")

    try:
        # Step 1: Combine STARTER_MEMES with Remote List if available
        all_memes = STARTER_MEMES.copy()
        try:
            remote_res = requests.get(MEME_REPO, timeout=3)
            if remote_res.status_code == 200:
                remote_memes = [m.strip() for m in remote_res.text.split('\n') if m.strip()]
                all_memes.extend(remote_memes)
        except: pass

        # 🔄 Anti-Repeat Logic
        available_memes = [m for m in all_memes if m not in RECENT_MEMES]
        
        if not available_memes:
            RECENT_MEMES.clear()
            available_memes = all_memes

        selected_meme = random.choice(available_memes)
        
        # Update Memory (Last 30)
        RECENT_MEMES.append(selected_meme)
        if len(RECENT_MEMES) > 30:
            RECENT_MEMES.pop(0)

        # 🚀 Send as Media & Delete Cmd
        await event.delete()
        await event.client.send_file(event.chat_id, selected_meme, reply_to=event.reply_to_msg_id)

    except Exception as e:
        await event.edit(f"❌ `Error: {str(e)}`")

# ================= SETUP =================
async def setup(client):
    client.add_event_handler(meme_cmd)

