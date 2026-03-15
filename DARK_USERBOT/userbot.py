import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from config import API_ID, API_HASH
from database import get_all_sessions
import importlib
from pathlib import Path

# Hosted clients ki list
clients = []

async def start_userbots():
    sessions = await get_all_sessions()
    print(f"Found {len(sessions)} sessions in database. Starting...")

    for session_str in sessions:
        try:
            client = TelegramClient(StringSession(session_str), API_ID, API_HASH)
            await client.connect()
            
            if await client.is_user_authorized():
                me = await client.get_me()
                print(f"✅ Started Userbot for: {me.first_name}")
                
                # Plugins load karna
                await load_plugins(client)
                clients.append(client)
            else:
                print("❌ Session expired or invalid.")
        except Exception as e:
            print(f"⚠️ Error starting client: {e}")

async def load_plugins(client):
    # Plugins folder se saari files read karna
    path = Path("plugins")
    for file in path.glob("*.py"):
        if file.name == "__init__.py":
            continue
        
        name = f"plugins.{file.stem}"
        plugin = importlib.import_module(name)
        
        # Plugin ko client ke saath register karna
        if hasattr(plugin, "setup"):
            await plugin.setup(client)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_userbots())
    print("All Userbots are now running.")
    loop.run_forever()
              
