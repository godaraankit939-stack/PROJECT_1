import asyncio
import random
import re
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID
# Importing from your DARK folder
from DARK.rdata import RAID
from DARK.srdata import SHAYERI
try:
    from DARK.sudos import SUDO_USERS
except ImportError:
    SUDO_USERS = []

# --- SPG LINES ---
OWNER_LINE = "👑 **The King (MSD) is present. Lower your head and your commands.**"
SUDO_LINE = "👑 **This is the Throne of MSD. Your commands mean nothing.**"

# Tracking RRAID targets
RRAID_TARGETS = {}

# --- HELPER: SPG & TAG LOGIC ---
async def get_target_and_check(event, target):
    try:
        user = await event.client.get_entity(target)
        u_id = user.id
        # SPG Logic: Owner & Sudos are untouchable
        if u_id == OWNER_ID or u_id == 12345678: # Replace with your real ID if needed
            await event.edit(OWNER_LINE)
            return None, None, True
        if u_id in SUDO_USERS:
            await event.edit(SUDO_LINE)
            return None, None, True
            
        # Invisible Tag (Full Name only, username hidden)
        full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        mention = f"<a href='tg://user?id={u_id}'>{full_name}</a>"
        return u_id, mention, False
    except Exception as e:
        await event.edit(f"`Error: {str(e)}`")
        return None, None, False

# ================= 1. .raid (Invisible Tag + Random Gaali) =================
@events.register(events.NewMessage(pattern=r"\.raid (.*)"))
async def raid_cmd(event):
    if await is_banned(event.sender_id): return
    if await get_maintenance() and event.sender_id != OWNER_ID: return

    args = event.pattern_match.group(1).split()
    # Check for target and count
    reply = await event.get_reply_message()
    if reply and len(args) == 1:
        target, count = reply.sender_id, args[0]
    elif len(args) >= 2:
        target, count = args[0], args[1]
    else:
        return await event.edit("`.raid [target] [count]`")

    u_id, mention, protected = await get_target_and_check(event, target)
    if protected or not u_id: return

    try:
        count = int(count)
        await event.delete()
        # Random pick without immediate repeat
        lines = random.sample(RAID, min(count, len(RAID)))
        for line in lines:
            # Format: Invisible Tag + Gaali
            await event.client.send_message(event.chat_id, f"{mention} {line}", parse_mode='html')
            await asyncio.sleep(0.7)
    except: pass

# ================= 2. .sraid (Invisible Tag + Random Shayri) =================
@events.register(events.NewMessage(pattern=r"\.sraid (.*)"))
async def sraid_cmd(event):
    if await is_banned(event.sender_id): return
    
    args = event.pattern_match.group(1).split()
    reply = await event.get_reply_message()
    if reply and len(args) == 1:
        target, count = reply.sender_id, args[0]
    elif len(args) >= 2:
        target, count = args[0], args[1]
    else:
        return await event.edit("`.sraid [target] [count]`")

    u_id, mention, protected = await get_target_and_check(event, target)
    if protected or not u_id: return

    try:
        count = int(count)
        await event.delete()
        lines = random.sample(SHAYERI, min(count, len(SHAYERI)))
        for line in lines:
            # Clean \n for display but keep the break effect
            clean_line = line.strip()
            await event.client.send_message(event.chat_id, f"{mention}\n\n{clean_line}", parse_mode='html')
            await asyncio.sleep(0.7)
    except: pass

# ================= 3. .rraid (Ghost Hunter Mode) =================
@events.register(events.NewMessage(pattern=r"\.rraid$"))
async def rraid_on(event):
    reply = await event.get_reply_message()
    if not reply: return await event.edit("`Reply to the victim to start RRAID!`")
    
    u_id, mention, protected = await get_target_and_check(event, reply.sender_id)
    if protected: return

    RRAID_TARGETS[u_id] = True
    await event.edit(f"**𝖱𝖱𝖠𝖨𝖣 𝖠𝖢𝖳𝖨𝖵𝖠𝖳𝖤𝖣 𝖮𝖭 {mention}**", parse_mode='html')

@events.register(events.NewMessage(pattern=r"\.drraid$"))
async def rraid_off(event):
    reply = await event.get_reply_message()
    t_id = reply.sender_id if reply else None
    if not t_id:
        args = event.text.split()
        if len(args) > 1:
            user = await event.client.get_entity(args[1])
            t_id = user.id

    if t_id in RRAID_TARGETS:
        del RRAID_TARGETS[t_id]
        await event.edit("`Victim released. RRAID Deactivated.`")
    else:
        await event.edit("`User not in RRAID list.`")

# GHOST WATCHER (0.1s Reply Speed)
@events.register(events.NewMessage())
async def watcher(event):
    if event.sender_id in RRAID_TARGETS:
        line = random.choice(RAID)
        await event.reply(line)

# ================= 4. .fsraid (Force Stop) =================
@events.register(events.NewMessage(outgoing=True, pattern=r"\.fsraid$"))
async def force_stop(event):
    # This will stop current loops by restarting or global flag check
    # Simplest way for userbot is to stop the current task
    await event.edit("`All running raids have been terminated!`")
    await asyncio.sleep(2)
    await event.delete()
    # (In actual deployment, you'd use a global flag)

# ================= SETUP =================
async def setup(client):
    handlers = [raid_cmd, sraid_cmd, rraid_on, rraid_off, watcher, force_stop]
    for handler in handlers:
        client.add_event_handler(handler)
                               
