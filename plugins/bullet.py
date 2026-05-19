import asyncio
import time
import random
from telethon import events
from database import get_maintenance, is_banned
from config import OWNER_ID

# --- DYNAMIC SUDO IMPORT ---
try:
    from DARK.sudos import SUDO_USERS
except ImportError:
    SUDO_USERS = []

# Global Flag for Bullet Stop
BULLET_RUNNING = True

# 20+ Random Winning Lines for Giveaway Bypass
WINNING_MESSAGES = [
    "I am the winner!", "Give me premium!", "Claiming my reward!", 
    "Top 1 is mine!", "GG easy win!", "Fastest comment here!", 
    "Premium belongs to me!", "Boom! Done.", "I am first!", 
    "Check the list, I won!", "Victory is mine!", "Unstoppable speed!", 
    "Giveaway champion!", "Direct hit!", "Boom baby!", 
    "Let's gooo winner!", "Target locked, won!", "Got the top spot!", 
    "Premium incoming!", "Speed of light!", "Winner winner!", 
    "The crown is mine!", "Fastest fingers!", "Done and dusted!"
]

# ================= BULLET SPEED SPAM PLUGIN =================
# Pattern handles both: `.bullet 15` AND `.bullet 15 Hello`
@events.register(events.NewMessage(pattern=r"\.bullet (\d+)(?:\s+(.*))?"))
async def bullet_speed_spam(event):
    global BULLET_RUNNING
    
    # 🛡️ SAFETY & PRIVACY CHECKS
    if event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        await event.edit("**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤𝖣** 🛡️")
        return
    if await is_banned(event.sender_id): return
    if await get_maintenance() and event.sender_id != OWNER_ID: return

    # Arguments Parse
    count = int(event.pattern_match.group(1))
    custom_text = event.pattern_match.group(2)
    
    # Command trigger hote hi message delete taaki clear screen rahe
    await event.delete()
    BULLET_RUNNING = True
    
    # 1 Second me ~13 msgs ke liye exact 0.072s ka interval math perfectly set hai
    bullet_delay = 0.072 
    
    print(f"🚀 [BULLET ACTIVATED] Sending {count} messages...")

    for i in range(count):
        if not BULLET_RUNNING:
            break
        
        # Agar text nahi diya, toh random list se uthayega (Bypass Anti-Spam)
        if custom_text:
            msg_to_send = custom_text
        else:
            msg_to_send = random.choice(WINNING_MESSAGES)
            
        # 🔥 ULTRA FAST: Bina network server response ka wait kiye background task fire hoga
        asyncio.create_task(event.client.send_message(event.chat_id, msg_to_send))
        
        # Strict micro-sleep for keeping the 1-second target stable
        if i < count - 1:
            await asyncio.sleep(bullet_delay)

    print("✅ [BULLET FINISHED] All tasks successfully pushed to Telegram queue.")

# ================= SETUP FUNCTION =================
async def setup(client):
    client.add_event_handler(bullet_speed_spam)
    
