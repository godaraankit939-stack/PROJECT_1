import asyncio
import random
import requests
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"

def get_remote_aura():
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

    # 🛡️ OWNER PROTECTION
    if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        aura_list = get_remote_aura()
        selected_aura = random.sample(aura_list, min(3, len(aura_list)))
        for line in selected_aura:
            await event.edit(line)
            await asyncio.sleep(1.5)
        return

    # 🚫 BAN CHECK
    if await is_banned(event.sender_id):
        return

    # 🛠️ MAINTENANCE
    if await get_maintenance() and event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
        return await event.edit("`System Status: Maintenance Mode Active.`")
    
    # 🔐 AUTH CHECK
    if event.sender_id != me.id and not await is_sudo(event.sender_id):
        return await event.edit("`Not allowed.`")

    song_name = event.pattern_match.group(1).strip()
    if not song_name:
        return await event.edit("`Error: Please provide a song name (e.g., .lyrics Daku).`")

    await event.edit(f"`🎵 Searching lyrics for: {song_name}...`")

    lyrics_text = None
    title = song_name.upper()
    artist = "Unknown Artist"

    try:
        # 🎵 SOURCE 1 (Lyrist)
        try:
            api_url = "https://lyrist.vercel.app/api/" + song_name.replace(' ', '%20')
            res = requests.get(api_url, timeout=5)

            if res.status_code == 200:
                data = res.json()
                if data.get("lyrics"):
                    lyrics_text = data["lyrics"]
                    title = data.get("title", title)
                    artist = data.get("artist", artist)
        except:
            pass

        # 🎵 SOURCE 2 (Fallback)
        if not lyrics_text:
            try:
                url = "https://api.lyrics.ovh/v1//" + song_name
                res = requests.get(url, timeout=5)

                if res.status_code == 200:
                    data = res.json()
                    if data.get("lyrics"):
                        lyrics_text = data["lyrics"]
            except:
                pass

        # ❌ FINAL FAIL
        if not lyrics_text:
            return await event.edit("`Error: No lyrics found for this song.`")

        # 🎨 OUTPUT FORMAT
        header = "╔══════════════════╗\n║  ❁ 𝖫𝖸𝖱𝖨𝖢𝖲 𝖥𝖮𝖴𝖭𝖣 ❁  ║\n╚══════════════════╝\n"
        meta = "**Song:** `" + str(title) + "`\n**Artist:** `" + str(artist) + "`\n\n"
        
        if len(lyrics_text) > 3500:
            lyrics_text = lyrics_text[:3500] + "\n... (Lyrics truncated)"
            
        code_block = "```\n" + str(lyrics_text) + "\n```"
        
        final_msg = header + meta + code_block + "\n\n**Powered By DARK-USERBOT** 💀"

        await event.edit(final_msg)

    except Exception as e:
        await event.edit("❌ **Lyrics Failure:** `" + str(e) + "`")

async def setup(client):
    client.add_event_handler(lyrics_handler)
