import asyncio
from os import environ
from telethon import events
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream

# --- CORE LOGIC BINDING ---
# Main client module ko access karne ke liye (Aapke bot ke main file ke mutabik automatically bind hoga)
try:
    from __main__ import bot as client
except ImportError:
    try:
        from config import bot as client
    except ImportError:
        # Agar default import na mile toh session se dynamic extraction ke liye backup
        client = None

ASSISTANT_SESSION = environ.get("ASSISTANT_SESSION", "your_assistant_string_session_here")

# Initialize assistant inside telethon context
from pyrogram import Client as PyroClient
assistant_client = PyroClient("AssistantMusic", session_string=ASSISTANT_SESSION)
call_engine = PyTgCalls(assistant_client)

group_music_queue = {}

# --- CORE UTILITY PIPELINES ---

async def fetch_premium_audio(query: str):
    import yt_dlp
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
            metadata.get("duration", 0)
        )

async def execute_sequential_join(event, chat_id: int):
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

# --- TELETHON COMMAND LISTENER (AUDIO ONLY) ---

# .play command handle mapping for telethon (Only matching deployer instance)
if client:
    @client.on(events.NewMessage(pattern=r"^\.play(?:\s+(.*))?$", outgoing=True))
    async def play_stream_router(event):
        chat_id = event.chat_id
        search_query = event.pattern_match.group(1)
        
        if not search_query:
            await event.edit("❌ **Usage Format:** `.play [Track Name / YouTube URL]`")
            return

        tracking_panel = await event.edit("🔍 **Searching Audio...**")
        
        try:
            audio_node, track_title, track_len = await fetch_premium_audio(search_query)
            await tracking_panel.edit(f"✨ **Audio Found:** `{track_title}`\n🛰️ Checking Assistant...")
        except Exception as error:
            await tracking_panel.edit(f"❌ **Audio Scraping Failed:** `{str(error)}`")
            return

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
            "audio": audio_node,
            "duration": track_len
        })

        if len(group_music_queue[chat_id]) == 1:
            await stream_initialization_pipeline(chat_id, tracking_panel)
        else:
            await tracking_panel.edit(f"📥 **Queued at Position #{len(group_music_queue[chat_id])}:** `{track_title}`")

    @client.on(events.NewMessage(pattern=r"^\.skip$", outgoing=True))
    async def skip_track_trigger(event):
        action_panel = await event.edit("⏭️ **Processing Skip Signal...**")
        await process_track_skip(event.chat_id, action_panel)

async def stream_initialization_pipeline(chat_id: int, tracking_panel):
    if chat_id not in group_music_queue or not group_music_queue[chat_id]:
        return

    active_track = group_music_queue[chat_id][0]
    stream_spec = MediaStream(active_track["audio"])

    try:
        if not call_engine.is_connected:
            await call_engine.start()
        
        await call_engine.join_group_call(chat_id, stream_spec)
        
        dashboard_text = (
            f"🎵 **Now Playing Premium Audio Stream**\n\n"
            f"🔹 **Title:** `{active_track['title']}`\n"
            f"🔹 **Type:** High-Fidelity Audio Feed\n\n"
            f"⚙️ _Powered by DARK USERBOT ENGINE_"
        )
        await tracking_panel.edit(dashboard_text)
    except Exception as error:
        await tracking_panel.edit(f"❌ **Audio Mount Failed:** `{str(error)}`")
        await process_track_skip(chat_id, tracking_panel)

async def process_track_skip(chat_id: int, tracking_panel):
    if chat_id in group_music_queue and group_music_queue[chat_id]:
        group_music_queue[chat_id].pop(0)

    if chat_id in group_music_queue and group_music_queue[chat_id]:
        try:
            next_spec = MediaStream(group_music_queue[chat_id][0]["audio"])
            await call_engine.change_stream(chat_id, next_spec)
            await stream_initialization_pipeline(chat_id, tracking_panel)
        except Exception:
            await call_engine.leave_group_call(chat_id)
            await stream_initialization_pipeline(chat_id, tracking_panel)
    else:
        try:
            await call_engine.leave_group_call(chat_id)
            await assistant_client.leave_chat(chat_id)
        except Exception:
            pass
        if chat_id in group_music_queue:
            del group_music_queue[chat_id]
        await tracking_panel.edit("⏹️ **Queue empty. Assistant client has disconnected.**")
      
