from telethon import events, functions
from userbot import client

import asyncio
from os import environ
from pyrogram import Client as PyroClient
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
import yt_dlp

# ================= CONFIG ================= #

ASSISTANT_SESSION = environ.get("ASSISTANT_SESSION")
ASSISTANT_USERNAME = "@SIRxMSD"

assistant = PyroClient("assistant", session_string=ASSISTANT_SESSION)
call = PyTgCalls(assistant)

QUEUE = {}
CURRENT = {}
PREVIOUS = {}

ASSISTANT_STARTED = False

# ================= CORE ================= #

async def start_assistant():
    global ASSISTANT_STARTED
    if not ASSISTANT_STARTED:
        await assistant.start()
        await call.start()
        ASSISTANT_STARTED = True

async def ensure_assistant(chat_id):
    try:
        await client(functions.channels.InviteToChannelRequest(
            channel=chat_id,
            users=[ASSISTANT_USERNAME]
        ))
    except:
        pass

async def get_audio(query):
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "nocheckcertificate": True,
        "default_search": "ytsearch"
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ydl.extract_info(query, download=False)
        )
        if "entries" in data:
            data = data["entries"][0]
        return data["url"], data["title"]

async def join_and_play(chat_id, url):
    await start_assistant()
    stream = MediaStream(url)
    await call.join_group_call(chat_id, stream)

def add_queue(chat_id, data):
    if chat_id not in QUEUE:
        QUEUE[chat_id] = []
    QUEUE[chat_id].append(data)

async def play_next(chat_id):
    if chat_id in QUEUE and QUEUE[chat_id]:
        song = QUEUE[chat_id].pop(0)
        CURRENT[chat_id] = song
        await join_and_play(chat_id, song["url"])
        return song
    return None

# ================= COMMANDS ================= #

# ▶️ PLAY
@client.on(events.NewMessage(pattern=r"\.play(?:\s+(.*))?"))
async def play_cmd(event):
    chat_id = event.chat_id
    user = await event.get_sender()

    try:
        query = event.text.split(None, 1)[1]
    except:
        return await event.reply("❌ Usage: `.play song name`")

    msg = await event.reply("🔍 Searching...")

    try:
        url, title = await get_audio(query)
    except Exception as e:
        return await msg.edit(f"❌ Error: {e}")

    data = {
        "title": title,
        "url": url,
        "user": user.first_name
    }

    await ensure_assistant(chat_id)

    if chat_id not in CURRENT:
        CURRENT[chat_id] = data
        await join_and_play(chat_id, url)

        await msg.edit(
            f"🎵 **Now Playing:** `{title}`\n"
            f"👤 Requested by: {user.first_name}\n"
            f"⚡ Powered by DARK USERBOT"
        )
    else:
        add_queue(chat_id, data)
        await msg.edit(
            f"📥 Added to Queue:\n`{title}`\n"
            f"⚡ Powered by DARK USERBOT"
        )

# ⏭ SKIP
@client.on(events.NewMessage(pattern=r"\.skip"))
async def skip_cmd(event):
    chat_id = event.chat_id

    if chat_id in CURRENT:
        PREVIOUS[chat_id] = CURRENT[chat_id]

    song = await play_next(chat_id)

    if song:
        await event.reply(
            f"⏭ Skipped\n🎵 Now Playing: `{song['title']}`\n⚡ Powered by DARK USERBOT"
        )
    else:
        await event.reply("❌ Queue empty")

# ⏮ PREVIOUS
@client.on(events.NewMessage(pattern=r"\.prev"))
async def prev_cmd(event):
    chat_id = event.chat_id

    if chat_id in PREVIOUS:
        song = PREVIOUS[chat_id]
        CURRENT[chat_id] = song
        await join_and_play(chat_id, song["url"])

        await event.reply(
            f"⏮ Previous:\n🎵 `{song['title']}`\n⚡ Powered by DARK USERBOT"
        )
    else:
        await event.reply("❌ No previous song")
