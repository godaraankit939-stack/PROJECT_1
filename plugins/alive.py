from import asyncio
import random
import requests
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

# --- GITHUB CONFIG ---
# GitHub pe file bana kar uska "RAW" link yahan paste karo
AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"

def get_remote_aura():
    try:
        response = requests.get(AURA_URL)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except:
        pass
    # Backup agar GitHub down ho
    return ["**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤𝖭𝖨𝖤𝖣** 🛡️", "⌬ `System: God Mode Active` ✨"]

ALIVE_TEXT = (
    "**⌬ 𝖣𝖠𝖱𝖪-𝖴𝖲𝖤𝖱𝖡𝖮𝖳 𝖨𝖲 𝖠𝖫𝖨𝖵𝖤 ⚡**\n\n"
    "◈ **𝖵𝖾𝗋𝗌𝗂𝗈𝗇:** `𝟩.𝟢 (𝖳𝗁𝖺𝗅𝖺 𝖥𝗈𝗋 𝖠 𝖱𝖾𝖺𝗌𝗈𝗇)`\n"
    "◈ **𝖲𝗍𝖺𝗍𝗎𝗌:** `𝖱𝖾𝖺𝖽𝗒 𝗍𝗈 𝖣𝖾𝗌𝗍𝗋𝗈𝗒` 💀"
)

async def setup(client):
    @client.on(events.NewMessage(pattern=r"\.alive"))
    async def alive_handler(event):
        me = await event.client.get_me()
        
        # --- OWNER PROTECTION SYSTEM ---
        if event.sender_id != me.id:
            if event.is_private:
                aura_list = get_remote_aura()
                # 3 Random lines select karna
                selected_aura = random.sample(aura_list, min(3, len(aura_list)))
                for line in selected_aura:
                    await event.reply(line)
                    await asyncio.sleep(1)
            return
        # --- PROTECTION END ---

        # 1. BAN CHECK
        if await is_banned(event.sender_id):
            return

        # 2. MAINTENANCE CHECK
        if await get_maintenance():
            if event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
                return await event.edit("🛠 **Maintenance Mode is ON.**")

        await event.edit(ALIVE_TEXT)
        
