import asyncio
from telethon import events

# --- EKDAM SIMPLE TEST HANDLER ---
# Pattern: .test likhne par animation hona chahiye
@events.register(events.NewMessage(pattern=r"^\.test$", outgoing=True))
async def test_animation(event):
    await event.edit("🚀 `Starting Test...`")
    await asyncio.sleep(1)
    
    for i in ["🔴", "🟡", "🟢", "✨ **TEST SUCCESSFUL!**"]:
        await event.edit(i)
        await asyncio.sleep(1)

# --- SETUP FUNCTION (Connects with main.py) ---
async def setup(client):
    client.add_event_handler(test_animation)
    print("✅ DEBUG: Animation Plugin Loaded Successfully!")
  
