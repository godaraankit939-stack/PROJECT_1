import asyncio
from os import environ
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from os import environ

# --- UNIVERSAL ENGINE CONFIGURATION ---
ASSISTANT_SESSION = environ.get("ASSISTANT_SESSION", "your_assistant_string_session_here")

# Initialize the secondary assistant client dynamically
assistant_client = Client("AssistantMusic", session_string=ASSISTANT_SESSION)
call_engine = PyTgCalls(assistant_client)

# Global memory allocation for tracking group queues
group_music_queue = {}

# --- CORE UTILITY PIPELINES ---

async def fetch_premium_stream(query: str, video_mode: bool = False):
    """Scrapes maximum quality direct streaming nodes using yt-dlp layer."""
    import yt_dlp
    ydl_config = {
        "format": "bestvideo+bestaudio/best" if video_mode else "bestaudio/best",
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
            metadata.get("url") if video_mode else None,
            metadata.get("title", "Premium Track"),
            metadata.get("duration", 0)
        )

async def execute_sequential_join(main_client, chat_id: int):
    """Executes the 3-Option Automatic Join Logic sequentially."""
    try:
        bot_peer = await assistant_client.get_me()
        await main_client.add_chat_members(chat_id, bot_peer.id)
        return True
    except Exception:
        try:
            invite_url = await main_client.export_chat_invite_link(chat_id)
            await assistant_client.join_chat(invite_url)
            return True
        except Exception:
            try:
                target_chat = await main_client.get_chat(chat_id)
                if target_chat.username:
                    await assistant_client.join_chat(target_chat.username)
                    return True
            except Exception:
                return False
    return False

def generate_dashboard_controls():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Pause ⏸️", callback_data="music_pause"),
            InlineKeyboardButton("Skip ⏭️", callback_data="music_skip"),
            InlineKeyboardButton("Stop ⏹️", callback_data="music_stop")
        ]
    ])

# --- DYNAMIC PLUGINS (TRIGGERED ONLY BY THE RESPECTIVE USERBOT DEPLOYER) ---

@Client.on_message(filters.command(["play", "vplay"], prefixes=".") & filters.me)
async def play_stream_router(client: Client, message: Message):
    chat_id = message.chat.id
    video_requested = message.command[0] == "vplay"
    
    if len(message.command) < 2:
        await message.edit("❌ **Usage Format:** `.play` or `.vplay` [Track Name / URL]")
        return

    search_query = message.text.split(None, 1)[1]
    
    tracking_panel = await message.edit("🔍 **Searching**")
    await asyncio.sleep(1.2)
    await tracking_panel.edit("🔍 **Searching.**")
    await asyncio.sleep(1.2)
    await tracking_panel.edit("🔍 **Searching..**")
    
    try:
        audio_node, video_node, track_title, track_len = await fetch_premium_stream(search_query, video_mode=video_requested)
        await tracking_panel.edit("✨ **Track Found!**")
        await asyncio.sleep(1)
    except Exception as error:
        await tracking_panel.edit(f"❌ **Metadata Scraping Failed:** `{str(error)}`")
        return

    try:
        await assistant_client.get_chat_member(chat_id, "me")
    except Exception:
        await tracking_panel.edit("🛰️ **Deploying Assistant Client to Destination...**")
        is_deployed = await execute_sequential_join(client, chat_id)
        if not is_deployed:
            await tracking_panel.edit("❌ **Automation Crash:** Assistant unable to clear join barriers.")
            return

    if chat_id not in group_music_queue:
        group_music_queue[chat_id] = []

    group_music_queue[chat_id].append({
        "title": track_title,
        "audio": audio_node,
        "video": video_node,
        "is_video": video_requested,
        "duration": track_len,
        "author": message.from_user.mention,
        "owner_id": message.from_user.id
    })

    if len(group_music_queue[chat_id]) == 1:
        await stream_initialization_pipeline(chat_id, tracking_panel)
    else:
        await tracking_panel.edit(f"📥 **Queued at Position #{len(group_music_queue[chat_id])}:** `{track_title}`")

async def stream_initialization_pipeline(chat_id: int, tracking_panel: Message):
    if chat_id not in group_music_queue or not group_music_queue[chat_id]:
        return

    active_track = group_music_queue[chat_id][0]
    
    # Version 3.x Universal Unified MediaStream Mapper
    if active_track["is_video"]:
        stream_spec = MediaStream(
            active_track["audio"],
            video_path=active_track["video"],
            video_width=1920,
            video_height=1080,
            video_fps=30
        )
    else:
        stream_spec = MediaStream(active_track["audio"])

    try:
        if not call_engine.is_connected:
            await call_engine.start()
        await call_engine.join_group_call(chat_id, stream_spec)
        
        dashboard_text = (
            f"🎵 **Now Playing Premium HD Stream**\n\n"
            f"🔹 **Title:** `{active_track['title']}`\n"
            f"🔹 **Resolution Type:** {'1080p Video Feed' if active_track['is_video'] else 'High-Fidelity Audio Feed'}\n"
            f"🔹 **Requested By:** {active_track['author']}\n\n"
            f"⚙️ _Powered by DARK USERBOT ENGINE_"
        )
        await tracking_panel.edit(dashboard_text, reply_markup=generate_dashboard_controls())
    except Exception as error:
        await tracking_panel.edit(f"❌ **Stream Mount Failed:** `{str(error)}`")
        await process_track_skip(chat_id, tracking_panel)

@Client.on_message(filters.command("skip", prefixes=".") & filters.me)
async def skip_track_trigger(client: Client, message: Message):
    action_panel = await message.edit("⏭️ **Processing Skip Signal...**")
    await process_track_skip(message.chat.id, action_panel)

async def process_track_skip(chat_id: int, tracking_panel: Message):
    if chat_id in group_music_queue and group_music_queue[chat_id]:
        group_music_queue[chat_id].pop(0)

    if chat_id in group_music_queue and group_music_queue[chat_id]:
        try:
            if group_music_queue[chat_id][0]["is_video"]:
                next_spec = MediaStream(
                    group_music_queue[chat_id][0]["audio"],
                    video_path=group_music_queue[chat_id][0]["video"],
                    video_width=1920,
                    video_height=1080,
                    video_fps=30
                )
            else:
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
        await tracking_panel.edit("⏹️ **Queue empty. Assistant client has disconnected and exited the channel instantly.**")

# --- INTERACTIVE INTERFACE ROUTERS (DYNAMIC OWNER LOCK) ---

@assistant_client.on_callback_query(filters.regex(r"^music_"))
async def music_dashboard_callback(client: Client, callback_query: CallbackQuery):
    target_chat = callback_query.message.chat.id
    
    if target_chat not in group_music_queue or not group_music_queue[target_chat]:
        await callback_query.answer("❌ No active playlist found for this chat.", show_alert=True)
        return
        
    allowed_user_id = group_music_queue[target_chat][0]["owner_id"]
    if callback_query.from_user.id != allowed_user_id:
        await callback_query.answer("❌ Access Denied: Only the Userbot Deployer can manage this playback.", show_alert=True)
        return

    control_action = callback_query.data.split("_")[1]

    if control_action == "pause":
        await call_engine.pause_stream(target_chat)
        await callback_query.answer("Playback Paused ⏸️")
    elif control_action == "skip":
        await callback_query.answer("Executing Track Skip ⏭️")
        await process_track_skip(target_chat, callback_query.message)
    elif control_action == "stop":
        await callback_query.answer("Terminating Session ⏹️")
        try:
            await call_engine.leave_group_call(target_chat)
            await assistant_client.leave_chat(target_chat)
        except Exception:
            pass
        if target_chat in group_music_queue:
            del group_music_queue[target_chat]
        await callback_query.message.edit("⏹️ **Stream session terminated. Assistant client disconnected successfully.**")
    
