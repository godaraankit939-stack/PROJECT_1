import asyncio
from os import environ
import yt_dlp
from telethon import events
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream

# Database functions import (Aapke framework ke mutabik)
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

# --- PYTGCALLS ASSISTANT CONFIGURATION ---
ASSISTANT_SESSION = environ.get("ASSISTANT_SESSION", "")

# Initialize Pyrogram Assistant inside Telethon plugin context
from pyrogram import Client as PyroClient
assistant_client = PyroClient("AssistantMusic", session_string=ASSISTANT_SESSION)
call_engine = PyTgCalls(assistant_client)

# Global memory allocation for tracking group queues
group_music_queue = {}

# --- CORE UTILITY PIPELINES ---

async def fetch_premium_audio(query: str):
    """Scrapes maximum quality direct audio streaming nodes using yt-dlp layer."""
    ydl_config = {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "default_search": "ytsearch",
        "source_address": "0.0.0.0",
    }
    with yt_dlp.YoutubeDL(ydl_config) as ydl:
        loop = asyncio.get_event_loop()
        metadata = await loop.run_in_executor(None, lambda: ydl.extract_info(query, download=False))
        if "entries" in metadata:
            metadata = metadata["entries"][0]
        
        return (
            metadata.get("url"),
            metadata.get("title", "Premium Track"),
        )

async def execute_sequential_join(event, chat_id: int):
    """Handles Assistant group joining routines dynamically."""
    try:
        bot_peer = await assistant_client.get_me()
        await event.client.add_chat_members(chat_id, bot_peer.id)
        return True
    except Exception:
        try:
            from telethon.tl.functions.channels import ExportInviteRequest
            invite = await event.client(ExportInviteRequest(chat_id))
            await assistant_client.join_chat(invite.link)
            return True
        except Exception:
            try:
                entity = await event.client.get_entity(chat_id)
                if getattr(entity, 'username', None):
                    await assistant_client.join_chat(entity.username)
                    return True
            except Exception:
                return False

async def process_track_skip(chat_id: int, tracking_panel):
    """Manages internal queue mapping and track shifting."""
    if chat_id in group_music_queue and group_music_queue[chat_id]:
        group_music_queue[chat_id].pop(0)

    if chat_id in group_music_queue and group_music_queue[chat_id]:
        try:
            next_spec = MediaStream(group_music_queue[chat_id][0]["audio"])
            await call_engine.change_stream(chat_id, next_spec)
            await tracking_panel.edit(f"🎵 **Next Track:** `{group_music_queue[chat_id][0]['title']}`")
        except Exception:
            await call_engine.leave_group_call(chat_id)
    else:
        try:
            await call_engine.leave_group_call(chat_id)
            await assistant_client.leave_chat(chat_id)
        except Exception:
            pass
        if chat_id in group_music_queue:
            del group_music_queue[chat_id]
        await tracking_panel.edit("⏹️ **Queue empty. Assistant client has disconnected.**")

# --- DARK-USERBOT FRAMEWORK SETUP FUNCTION ---

async def setup(client):
    
    # 1. PLAY COMMAND
    @client.on(events.NewMessage(pattern=r"^\.play(?:\s+(.*))?$"))
    async def play_handler(event):
        # Security checks (Framework Standard)
        if await is_banned(event.sender_id):
            return
        if await get_maintenance():
            if event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
                return await event.edit("🛠 **Maintenance Mode is ON.**")

        chat_id = event.chat_id
        # Extract track name/URL
        try:
            search_query = event.text.split(None, 1)[1]
        except Exception:
            await event.edit("❌ **Usage Format:** `.play [Track Name / YouTube URL]`")
            return

        tracking_panel = await event.edit("🔍 **Searching Audio...**")
        
        try:
            audio_node, track_title = await fetch_premium_audio(search_query)
            await tracking_panel.edit(f"✨ **Found:** `{track_title}`\n🛰️ Checking Assistant...")
        except Exception as error:
            await tracking_panel.edit(f"❌ **Audio Scraping Failed:** `{str(error)}`")
            return

        # Assistant visibility deployment
        try:
            await assistant_client.get_chat_member(chat_id, "me")
        except Exception:
            await tracking_panel.edit("🛰️ **Deploying Assistant Client to Destination...**")
            is_deployed = await execute_sequential_join(event, chat_id)
            if not is_deployed:
                await tracking_panel.edit("❌ **Automation Crash:** Assistant unable to clear join barriers.")
                return

        if chat_id not in group_music_queue:
            group_music_queue[chat_id] = []

        group_music_queue[chat_id].append({
            "title": track_title,
            "audio": audio_node
        })

        if len(group_music_queue[chat_id]) == 1:
            stream_spec = MediaStream(audio_node)
            try:
                if not call_engine.is_connected:
                    await call_engine.start()
                await call_engine.join_group_call(chat_id, stream_spec)
                await tracking_panel.edit(
                    f"🎵 **Now Playing Premium Audio**\n\n"
                    f"🔹 **Title:** `{track_title}`\n\n"
                    f"⚙️ _Powered by DARK USERBOT ENGINE_"
                )
            except Exception as error:
                await tracking_panel.edit(f"❌ **Audio Mount Failed:** `{str(error)}`")
                await process_track_skip(chat_id, tracking_panel)
        else:
            await tracking_panel.edit(f"📥 **Queued at Position #{len(group_music_queue[chat_id])}:** `{track_title}`")

    # 2. SKIP COMMAND
    @client.on(events.NewMessage(pattern=r"^\.skip$"))
    async def skip_handler(event):
        if await is_banned(event.sender_id):
            return
        if await get_maintenance():
            if event.sender_id != OWNER_ID and not await is_sudo(event.sender_id):
                return
                
        action_panel = await event.edit("⏭️ **Processing Skip Signal...**")
        await process_track_skip(event.chat_id, action_panel)
