from telethon import events

@client.on(events.NewMessage(outgoing=True, pattern=r"^\.a on$"))
async def test_anti(event):
    await event.edit("✅ AntiPM Plugin Loaded & Working!")
    
