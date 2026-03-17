import asyncio
import random
import requests
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

# --- GITHUB CONFIG (Aura Lines) ---
AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"

def get_remote_aura():
    """Fetches aura lines with a timeout to prevent bot hangs."""
    try:
        response = requests.get(AURA_URL, timeout=5)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except Exception:
        pass
    return ["**⌬ 𝖠𝖢𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤𝖣** 🛡️"]

@events.register(events.NewMessage(pattern=r"\.lyrics ?(.*)"))
async def lyrics_handler(event):
    client = event.client
    me = await client.get_me()

    # 🛡️ 1. NO ENTRY LOGIC (Forceful Edit for Unauthorized Users in Owner Chat)
    if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        aura_list = get_remote_aura()
        selected_aura = random.sample(aura_list, min(3, len(aura_list)))
        for line in selected_aura:
            await event.edit(line)
            await asyncio.sleep(1.5)
        return

    # 🛠️ 2. BAN CHECK
    if await is_banned(event.sender_id):
        return

    # 🛠️ 3. MAINTENANCE CHECK
    if await get_maintenance() and event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
        return await event.edit("`System Status: Maintenance Mode Active.`")
    
    # 🛠️ 4. AUTHORIZATION CHECK (Only Owner or Sudo)
    if event.sender_id != me.id and not await is_sudo(event.sender_id):
        return

    song_name = event.pattern_match.group(1).strip()
    if not song_name:
        return await event.edit("`Error: Please provide a song name (e.g., .lyrics Daku).`")

    await event.edit(f"`🎵 Searching lyrics for: {song_name}...`")

    try:
        # Fetching lyrics from Lyrist API
        api_url = "https://lyrist.vercel.app/api/" + song_name.replace(' ', '%20')
        res = requests.get(api_url, timeout=10)
        
        if res.status_code != 200:
            return await event.edit("`Error: Lyrics source is currently unreachable.`")
            
        data = res.json()
        if "lyrics" not in data or not data["lyrics"]:
            return await event.edit("`Error: No lyrics found for this song.`")

        title = data.get("title", song_name.upper())
        artist = data.get("artist", "Unknown Artist")
        lyrics_text = data["lyrics"]

        # Construction of the final message using concatenation to avoid f-string issues
        header = "╔══════════════════╗\n║  ❁ 𝖫𝖸𝖱𝖨𝖢𝖲 𝖥𝖮𝖴𝖭𝖣 ❁  ║\n╚══════════════════╝\n"
        meta = "**Song:** `" + str(title) + "`\n**Artist:** `" + str(artist) + "`\n\n"
        
        # Limit lyrics length to avoid Telegram message limits
        if len(lyrics_text) > 3500:
            lyrics_text = lyrics_text[:3500] + "\n... (Lyrics truncated)"
            
        # Wrapping lyrics in a code block for a compact, professional look
        code_block = "```\n" + str(lyrics_text) + "\n```"
        
        final_msg = header + meta + code_block + "\n\n**Powered By DARK-USERBOT** 💀"
        await event.edit(final_msg)

    except Exception as e:
        await event.edit("❌ **Lyrics Failure:** `" + str(e) + "`")

async def setup(client):
    client.add_event_handler(lyrics_handler)
