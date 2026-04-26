import asyncio
import random
from telethon import events, functions, types

GOD_MODE = False

@events.register(events.NewMessage(pattern=r"\.god$"))
async def toggle_god(event):
    global GOD_MODE
    if event.sender_id != (await event.client.get_me()).id: return
    
    GOD_MODE = not GOD_MODE
    status = "ON 🔱" if GOD_MODE else "OFF 🟢"
    await event.edit(f"🔱 **GOD MODE: {status}**")
    
    if GOD_MODE:
        # Background task for Last Seen Freeze
        asyncio.create_task(freeze_logic(event.client))

async def freeze_logic(client):
    while GOD_MODE:
        try:
            # Ye status ko "Last seen recently" par lock karne ki koshish karega
            await client(functions.account.UpdateStatusRequest(offline=True))
        except: pass
        await asyncio.sleep(25) # Delay badha diya taaki server ignore na kare

@events.register(events.NewMessage(outgoing=True))
async def typing_spoof(event):
    if not GOD_MODE or event.text.startswith("."): return
    
    # Status options: Choose Sticker ya Playing Game
    actions = [
        types.SendMessageGamePlayAction(),
        types.SendMessageChooseStickerAction()
    ]
    try:
        await event.client(functions.messages.SetTypingRequest(
            peer=event.input_chat,
            action=random.choice(actions)
        ))
    except: pass

def setup(client):
    client.add_event_handler(toggle_god)
    client.add_event_handler(typing_spoof)
  
