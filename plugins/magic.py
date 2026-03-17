import asyncio
import random
import requests
import re
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

# ================= CONFIG =================
AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"
MAGIC_MODE = {"status": False}

# ================= AURA =================
def get_remote_aura():
    try:
        res = requests.get(AURA_URL, timeout=5)
        if res.status_code == 200:
            return [x.strip() for x in res.text.split("\n") if x.strip()]
    except:
        pass
    return ["**ACCESS DENIED 🛡️**"]

# ================= FONT =================
FONT_MAP = {chr(i): chr(i) for i in range(32, 127)}

FONT_MAP.update({
    'a': '𝖺','b': '𝖻','c': '𝖼','d': '𝖽','e': '𝖾','f': '𝖿','g': '𝗀','h': '𝗁',
    'i': '𝗂','j': '𝗃','k': '𝗄','l': '𝗅','m': '𝗆','n': '𝗇','o': '𝗈','p': '𝗉',
    'q': '𝗊','r': '𝗋','s': '𝗌','t': '𝗍','u': '𝗎','v': '𝗏','w': '𝗐','x': '𝗑',
    'y': '𝗒','z': '𝗓'
})

# ================= EMOJI MAP =================
EMOJI_MAP = {
    "love": "❤️", "hate": "🥀", "sad": "😢", "happy": "😊",
    "king": "👑", "money": "💰", "war": "⚔️", "kill": "💀",
    "danger": "⚠️", "power": "⚡", "fire": "🔥", "cool": "😎",
    "smart": "🧠", "dark": "🌑", "diamond": "💎", "win": "🏆",
    "bro": "🤜", "family": "🏡", "code": "💻", "bot": "🤖",

    # Hindi
    "pyar": "❤️", "nafrat": "🥀", "gussa": "💢",
    "dhokha": "💔", "dil": "❤️", "raja": "👑",
    "sher": "🦁", "aukat": "📏", "bhai": "🤜",
    "maut": "💀", "yaar": "🤝", "mahadev": "🔱"
}

# ================= FAKE AI MOOD =================
def detect_mood(text):
    text = text.lower()

    if any(x in text for x in ["haha", "lol", "fun", "enjoy"]):
        return "😊"
    if any(x in text for x in ["sad", "alone", "miss", "cry"]):
        return "😢"
    if any(x in text for x in ["angry", "idiot", "stupid"]):
        return "💢"
    if any(x in text for x in ["love", "baby", "jaan"]):
        return "❤️"
    if any(x in text for x in ["kill", "danger", "threat"]):
        return "⚠️"

    return ""

# ================= STYLIZE =================
def stylize(text):
    styled = "".join([FONT_MAP.get(c, c) for c in text])

    words = styled.split()
    final_words = []
    found_any = False

    for word in words:
        clean = re.sub(r'[^a-zA-Z]', '', word).lower()
        emoji = ""

        for key in EMOJI_MAP:
            if key in clean:
                emoji = EMOJI_MAP[key]
                found_any = True
                break

        final_words.append(word + emoji)

    result = " ".join(final_words)

    # 🧠 fallback mood
    if not found_any:
        mood = detect_mood(text)
        if mood:
            result += " " + mood

    return result

# ================= TOGGLE =================
@events.register(events.NewMessage(outgoing=True, pattern=r"\.magic$"))
async def toggle_magic(event):
    if await is_banned(event.sender_id):
        return

    if await get_maintenance() and event.sender_id != OWNER_ID:
        return

    MAGIC_MODE["status"] = not MAGIC_MODE["status"]

    status = "ON 🟢" if MAGIC_MODE["status"] else "OFF 🔴"
    await event.edit(f"`🪄 Magic Mode {status}`")
    await asyncio.sleep(1.5)
    await event.delete()

# ================= AUTO MAGIC =================
@events.register(events.NewMessage(outgoing=True))
async def auto_magic(event):

    # OWNER PROTECTION
    if event.is_private and event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        aura = get_remote_aura()
        for line in random.sample(aura, min(3, len(aura))):
            await event.edit(line)
            await asyncio.sleep(1.5)
        return

    if not MAGIC_MODE["status"]:
        return

    if not event.text:
        return

    if event.text.startswith("."):
        return

    if await is_banned(event.sender_id):
        return

    original = event.text
    new_text = stylize(original)

    if original != new_text:
        try:
            await event.edit(new_text)
        except:
            pass

# ================= SETUP =================
async def setup(client):
    client.add_event_handler(toggle_magic)
    client.add_event_handler(auto_magic)
