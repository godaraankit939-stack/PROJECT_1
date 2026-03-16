import time
from telethon import events
from database import get_maintenance, is_sudo, is_banned # is_banned yahan add kiya
from config import OWNER_ID

async def setup(client):
    @client.on(events.NewMessage(outgoing=True, pattern=r"\.ping"))
    async def ping_handler(event):
        # 1. BAN CHECK (Sabse Pehle)
        # Agar tumne kisi ko ban kiya hai, toh bot uske liye reply nahi karega
        if await is_banned(event.sender_id):
            return

        # 2. MAINTENANCE CHECK
        if await get_maintenance():
            # Owner aur Sudo ko maintenance affect nahi karegi
            if event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
                return await event.edit("🛠 **Maintenance Mode is ON.**")

        # --- Ping Calculation Logic ---
        start = time.time()
        msg = await event.edit("`Pinging...` ⚡")
        end = time.time()
        
        ping_time = round((end - start) * 1000, 2)
        
        # Final Minimal Ping Design (Locked by Ankit)
        response = (
            "**⌬ 𝖯𝖮𝖭𝖦!** 🏓\n\n"
            f"◈ **𝖲𝗉𝖾𝖾𝖽:** `{ping_time}ms`\n"
            f"◈ **𝖬𝗈𝖽𝖾:** `𝖠𝖼𝗍𝗂𝗏𝖾` ⚡"
        )
        await msg.edit(response)
      
