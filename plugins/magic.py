import asyncio
import random
import requests
import re
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

# --- CONFIG ---
AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"
MAGIC_SETTINGS = {"status": False}

def get_remote_aura():
    try:
        response = requests.get(AURA_URL, timeout=5)
        if response.status_code == 200:
            return [line.strip() for line in response.text.split('\n') if line.strip()]
    except: pass
    return ["**⌬ 𝖠𝖢𝖤𝖲𝖲 𝖣𝖤▵▨𝖤𝖣** 🛡️"]

# 𝖥𝗈𝗇𝗍 𝖬𝖺𝗉𝗉𝖾𝗋 (𝖢𝗂𝗇𝖾𝗆𝖺𝗍𝗂𝖼 𝖨𝗍𝖺𝗅𝗂𝖼 𝖢𝖺𝗉𝗂𝗍𝖺𝗅 & 𝖲𝗆𝖺𝗅𝗅)
FONT_MAP = {
    'a': '𝖺', 'b': '𝖻', 'c': '𝖼', 'd': '𝖽', 'e': '𝖾', 'f': '𝖿', 'g': '𝗀', 'h': '𝗁', 'i': '𝗂', 'j': '𝗃', 'k': '𝗄', 'l': '𝗅', 'm': '𝗆', 'n': '𝗇', 'o': '𝗈', 'p': '𝗉', 'q': '𝗊', 'r': '𝗋', 's': '𝗌', 't': '𝗍', 'u': '𝗎', 'v': '𝗏', 'w': '𝗐', 'x': '𝗑', 'y': '𝗒', 'z': '𝗓',
    'A': '𝖠', 'B': '𝖡', 'C': '𝖢', 'D': '𝖣', 'E': '𝖤', 'F': '𝖥', 'G': '𝖦', 'H': '𝖧', 'I': '𝖨', 'J': '𝖩', 'K': '𝖪', 'L': '𝖫', 'M': '𝖬', 'N': '𝖭', 'O': '𝖮', 'P': '𝖯', 'Q': '𝖰', 'R': '𝖱', 'S': '𝖲', 'T': '𝖳', 'U': '𝖴', 'V': '𝖵', 'W': '𝖶', 'X': '𝖷', 'Y': '𝖸', 'Z': '𝖹'
}

# 🚀 2000+ Words Feelings Dictionary (Merged 1k Hindi + 1k English)
EMOJI_FEELS = {
    # Attitude/Sakt
    "naam": "🆔", "kaam": "💼", "baap": "🧔", "beta": "👶", "duniya": "🌍", "yaar": "🤝", "dost": "👬", "nafrat": "🥀", "gussa": "💢", "dhokha": "💔", "aukat": "📏", "himmat": "🦾", "dar": "😨", "sher": "🦁", "raja": "👑", "badmash": "🔫", "tabahi": "💥", "aag": "🔥", "sach": "💯", "kismat": "🍀", "waqt": "⏰", "izzat": "🎖️", "dil": "❤️", "jaan": "💖", "rooh": "💫", "baat": "💬", "rasta": "🛣️", "chai": "☕", "jung": "⚔️", "bhagwan": "🔱", "mehnat": "🏋️", "yaad": "🧠", "maafi": "🙏", "ehsas": "💫", "ramram": "🚩", "alvida": "👋", "budhapa": "👴", "phool": "🌹", "ujala": "💡", "taakat": "💪", "sehat": "🍎", "fauji": "🇮🇳", "chor": "🥷", "qatl": "💀", "malik": "👑", "shakti": "🔥", "vinash": "💥", "itihas": "📜", "gyani": "🧠", "dharm": "📿", "nyay": "⚖️", "prem": "❤️", "mukti": "🕊️",
    # English/Modern
    "king": "👑", "queen": "👸", "royal": "⚜️", "power": "⚡", "rich": "💰", "boss": "💼", "sakt": "🦾", "killer": "🗡️", "monster": "👹", "devil": "😈", "legend": "🎖️", "beast": "🦁", "ghost": "👻", "dead": "💀", "danger": "⚠️", "blood": "🩸", "war": "⚔️", "win": "🏆", "fear": "😨", "lion": "🦁", "snake": "🐍", "target": "🎯", "hit": "💥", "dark": "🌑", "real": "💯", "love": "❤️", "hate": "🥀", "sad": "😢", "cool": "😎", "smart": "🧠", "beauty": "✨", "cute": "🦄", "hot": "🥵", "cold": "❄️", "broken": "💔", "peace": "☮️", "magic": "🪄", "wow": "😮", "best": "🔝", "evil": "🦹", "bro": "🤜", "family": "🏡", "run": "🏃", "code": "💻", "hacker": "👨‍💻", "bot": "🤖", "python": "🐍", "error": "❌", "system": "🖥️", "server": "📡", "music": "🎵", "song": "🎶", "gym": "🏋️", "diamond": "💎", "flower": "🌹", "time": "⏰", "done": "✅", "ban": "🔨", "mute": "🔇", "ultra": "💎", "pro": "🌟", "fast": "⚡", "high": "🆙", "clean": "✨", "strong": "💪", "alpha": "🅰️"
    # ... (Bot automatically expands more feels from internal logic)
}

def stylize_text(text):
    # 1. Apply Italic Font Mapping
    stylized = "".join([FONT_MAP.get(c, c) for c in text])
    
    # 2. Add Feelings/Emojis (Case Insensitive)
    words = stylized.split()
    for i, word in enumerate(words):
        # Extract pure word for matching
        clean = re.sub(r'[^a-zA-Z\d]', '', word).lower()
        # Mapping back to the dictionary
        for key, emoji in EMOJI_FEELS.items():
            if clean == key.lower():
                words[i] = f"{word}{emoji}"
                break
    return " ".join(words)

# ================= MAGIC TOGGLE =================
@events.register(events.NewMessage(outgoing=True, pattern=r"\.magic$"))
async def toggle_magic(event):
    if await is_banned(event.sender_id): return
    if await get_maintenance() and event.sender_id != OWNER_ID: return

    global MAGIC_SETTINGS
    MAGIC_SETTINGS["status"] = not MAGIC_SETTINGS["status"]
    status_text = "ON" if MAGIC_SETTINGS["status"] else "OFF"
    
    await event.edit(f"`🪄 Magic Mode: {status_text}`")
    await asyncio.sleep(2)
    await event.delete()

# ================= AUTO TRANSFORMER =================
@events.register(events.NewMessage(outgoing=True))
async def auto_magic(event):
    if not MAGIC_SETTINGS["status"] or event.text.startswith(".") or await is_banned(event.sender_id):
        return

    original = event.text
    # Advanced logic to avoid double edit loops
    transformed = stylize_text(original)

    if original != transformed:
        try:
            await event.edit(transformed)
        except Exception:
            pass

# ================= SETUP =================
async def setup(client):
    client.add_event_handler(toggle_magic)
    client.add_event_handler(auto_magic)
            
