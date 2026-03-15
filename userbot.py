import asyncio
import importlib
import os
import sys
from pathlib import Path
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Environment aur Database se imports
from config import API_ID, API_HASH, OWNER_ID
from database import get_all_sessions, get_maintenance, is_sudo

# Render fix: ensures config/database are found
sys.path.append(os.getcwd())

async def start_userbots():
    """Database se saare sessions uthakar ek saath start karne ke liye"""
    sessions = await get_all_sessions()
    
    if not sessions:
        print("ℹ️ No hosted sessions found in Database.")
        return

    print(f"🔥 Starting {len(sessions)} Userbots... Please wait.")

    for session_str in sessions:
        try:
            client = TelegramClient(StringSession(session_str), API_ID, API_HASH)
            await client.connect()

            if await client.is_user_authorized():
                me = await client.get_me()
                print(f"✅ Live: {me.first_name} (@{me.username})")

                # --- GLOBAL MAINTENANCE HANDLER ---
                @client.on(events.NewMessage(outgoing=True))
                async def global_maintenance_manager(event):
                    if await get_maintenance():
                        # Owner aur Sudo ko maintenance affect nahi karegi
                        if event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
                            if event.text.startswith("."):
                                await event.edit("🛠 **DARK-USERBOT is currently under Maintenance.**\nCommands are disabled for now.")
                                # Agle plugins ko execute hone se rokne ke liye
                                raise events.StopPropagation

                # --- DYNAMIC PLUGIN LOADER ---
                await load_plugins(client)
                
                # Client ko background task mein run karna
                asyncio.create_task(client.run_until_disconnected())
                
