import asyncio
from telethon import events, functions
from database import (
    is_banned, get_maintenance, is_approved, 
    approve_user, disapprove_user, get_antipm_status,
    is_warned_in_db, set_warned_in_db, delete_warned_user, set_antipm_status, is_sudo
)
from config import OWNER_ID

# --- 1. ANTIPM MESSAGE HANDLER ---
@events.register(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def antipm_handler(event):
    client = event.client
    me = await client.get_me()

    # 🛠 DIAGNOSTIC: Logs me check karo ye print ho rha hai ya nahi
    print(f"DEBUG: AntiPM Triggered by {event.sender_id}")

    if await is_banned(event.sender_id):
        return
    
    if await get_maintenance() and event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
        return

    # 🚨 CRITICAL CHECK: Agar ye False hai toh bot reply nahi dega
    status = await get_antipm_status()
    if not status:
        print("DEBUG: AntiPM is OFF in Database.")
        return 
        
    if event.sender_id == me.id or event.is_bot or await is_sudo(event.sender_id): 
        return
        
    if await is_approved(event.sender_id): 
        return 

    # --- LOGIC: WARN OR BLOCK ---
    is_warned = await is_warned_in_db(event.sender_id)
    if not is_warned:
        print(f"DEBUG: Sending First Warning to {event.sender_id}")
        warn_text = (
            "**⌬ 𝖠𝖭𝖳𝖨-𝖯𝖬 𝖲𝖤𝖢𝖴𝖱𝖨𝖳𝖸** 🛡️\n\n"
            "`Unauthorized Access Detected!`\n"
            "Do not message me in PM without permission. This is your **first and final warning**. "
            "One more message and you will be **Auto-Blocked**.\n\n"
            "**Status:** `Last Warning` ⚠️"
        )
        await event.reply(warn_text)
        await set_warned_in_db(event.sender_id)
    else:
        print(f"DEBUG: Blocking {event.sender_id}")
        block_text = (
            "**⌬ 𝖲𝖸𝖲▵𝖤𝖬 𝖡𝖫▮𝖢𝖪▵▨** 🚫\n\n"
            "`Access Denied!`\n"
            "You ignored the warning. You are now permanently blocked.\n\n"
            "**Goodbye!** 👋"
        )
        await event.reply(block_text)
        try:
            await client(functions.contacts.BlockRequest(id=event.sender_id))
            await delete_warned_user(event.sender_id)
        except Exception as e:
            print(f"DEBUG: Block Error: {e}")

# --- 2. ANTIPM COMMAND HANDLER ---
@events.register(events.NewMessage(outgoing=True, pattern=r"\.(antipm|approve|disapprove) ?(.*)"))
async def antipm_cmd_handler(event):
    if await is_banned(event.sender_id): return
    if await get_maintenance() and event.sender_id != OWNER_ID:
        return await event.edit("🛠 **Maintenance Mode is ON.**")
    
    if event.sender_id != (await event.client.get_me()).id and not await is_sudo(event.sender_id):
        return

    cmd = event.pattern_match.group(1)
    args = event.pattern_match.group(2).strip()

    if cmd == "antipm":
        if args == "on":
            await set_antipm_status(True)
            await event.edit("🛡️ **AntiPM Activated!**")
        elif args == "off":
            await set_antipm_status(False)
            await event.edit("🔓 **AntiPM Deactivated!**")
        else:
            await event.edit("`Usage: .antipm on/off`")
    
    elif cmd == "approve":
        reply = await event.get_reply_message()
        target = reply.sender_id if reply else args
        if not target: return await event.edit("`Reply to a user or give ID.`")
        await approve_user(target)
        await event.edit(f"✅ **User {target} Approved.**")
        
    elif cmd == "disapprove":
        reply = await event.get_reply_message()
        target = reply.sender_id if reply else args
        if not target: return await event.edit("`Reply to a user or give ID.`")
        await disapprove_user(target)
        await event.edit(f"❌ **User {target} Disapproved.**")

# --- SETUP FUNCTION ---
async def setup(client):
    client.add_event_handler(antipm_handler)
    client.add_event_handler(antipm_cmd_handler)
    
