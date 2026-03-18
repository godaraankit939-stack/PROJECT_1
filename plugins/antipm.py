import asyncio
import random
from telethon import events, functions, types
from database import (
    is_banned, get_maintenance, get_antipm_status,
    is_warned_in_db, set_warned_in_db, delete_warned_user, 
    is_sudo
)
from config import OWNER_ID

# --- NO ENTRY HELPER (Aura Lines) ---
def get_remote_aura():
    try:
        import requests
        AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"
        response = requests.get(AURA_URL, timeout=5)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except: pass
    return ["**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤𝖣** 🛡️"]

# ================= 1. THE AUTO-GUARD HANDLER =================
@events.register(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def antipm_handler(event):
    client = event.client
    sender_id = event.sender_id
    
    # 🛡️ 1. NO ENTRY LOGIC (Owner DM Protection)
    if event.chat_id == OWNER_ID and sender_id != OWNER_ID:
        aura_list = get_remote_aura()
        selected_aura = random.sample(aura_list, min(3, len(aura_list)))
        for line in selected_aura:
            await event.edit(line)
            await asyncio.sleep(1.5)
        return

    # 🛡️ 2. SECURITY CHECKS
    if await is_banned(sender_id): return
    if not await get_antipm_status(): return 

    # 👑 3. APG LOGIC (THE GOD MODE)
    # MSD (Owner) respects lines from config
    if sender_id == OWNER_ID:
        from config import APG_RESPECT
        await event.reply(random.choice(APG_RESPECT))
        return

    # 🛡️ 4. AUTO-ALLOW LOGIC (Sudos & Contacts)
    if event.is_bot or await is_sudo(sender_id): return
    
    try:
        full_user = await client(functions.users.GetFullUserRequest(id=sender_id))
        if full_user.phone_calls_available or full_user.private_forward_name:
            return
    except: pass

    # --- WARN & BLOCK LOGIC (The Sakt Way) ---
    if not await is_warned_in_db(sender_id):
        # Professional First Warning
        warn_msg = (
            "**⌬ 𝖠𝖭𝖳𝖨-𝖯𝖬 𝖲𝖤𝖢𝖴𝖱𝖨𝖳𝖸** 🛡️\n\n"
            "⚠️ `Warning:` Unauthorized DM detected!\n"
            "Please do not message me without permission. This is your only warning.\n\n"
            "**Next message will result in a permanent BLOCK.** 🚫"
        )
        await event.reply(warn_msg)
        await set_warned_in_db(sender_id)
    else:
        # Final Action: Block
        try:
            await event.reply("`Policy Violation: You have been BLOCKED for unauthorized DM.` 🚫")
            await asyncio.sleep(1)
            await client(functions.contacts.BlockRequest(id=sender_id))
            await delete_warned_user(sender_id)
        except: pass

# ================= 2. THE CONTROL COMMAND =================
@events.register(events.NewMessage(outgoing=True, pattern=r"^\.antipm (on|off)$"))
async def antipm_cmd(event):
    if await is_banned(event.sender_id):
        return await event.edit("`YOU WERE BANNED BY OWNER!`")
    
    mode = event.pattern_match.group(1).lower()
    from database import set_antipm_status
    
    if mode == "on":
        await set_antipm_status(True)
        await event.edit("🛡️ **Anti-PM Security: ACTIVATED**")
    else:
        await set_antipm_status(False)
        await event.edit("🔓 **Anti-PM Security: DEACTIVATED**")

# ================= SETUP =================
async def setup(client):
    client.add_event_handler(antipm_handler)
    client.add_event_handler(antipm_cmd)
    
