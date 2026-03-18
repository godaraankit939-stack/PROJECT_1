import asyncio
import random
from telethon import events

# --- 1. HELP MENU (.animation) ---
# Available for every bot user
ANIM_HELP = """
**👑 DARK-USERBOT ELITE ANIMATIONS 👑**

**🎭 Activity Movies:**
`.dino` `.fly` `.ufo` `.lift` `.fight` 
`.bottle` `.pro` `.propose` `.hero` `.nasa`

**🔥 Dark & Cyber:**
`.ghost` `.hack` `.nuke` `.cyber` `.error` 
`.server` `.virus` `.brain` `.toss`

**🔞 Extreme Set:**
`.bdsm` `.horny` `.blow` `.cum` `.pounding` 
`.climax` `.sexmsg` `.sex` `.face` `.strip`

**Usage:** Just type the command to start the movie!
"""

@events.register(events.NewMessage(pattern=r"^\.animation$"))
async def anim_help(event):
    await event.reply(ANIM_HELP)

# --- 2. THE MASTER HANDLER (PUBLIC ACCESS) ---
# NOTE: outgoing=True removed to allow ANY user to trigger
@events.register(events.NewMessage(pattern=r"^\.(ghost|hack|nuke|cyber|error|server|virus|bdsm|horny|blow|cum|pounding|climax|sexmsg|sex|face|strip|brain|toss|dino|fly|ufo|lift|fight|bottle|pro|propose|hero|nasa)$"))
async def master_anim_handler(event):
    cmd = event.pattern_match.group(1).lower()
    
    try:
        # --- 1. GHOST ---
        if cmd == "ghost":
            frames = [
                "⌬ 𝖲𝖢𝖠𝖭𝖭𝖨𝖭𝖦 𝖥𝖮𝖱 𝖫𝖨𝖥𝖤 𝖲𝖨𝖦𝖭𝖠𝖫𝖲... 🕵️",
                "⌬ 𝖳𝖤𝖬𝖯𝖤𝖱𝖠𝖳𝖴𝖱𝖤: -𝟣𝟢°𝖢 ❄️", "(  )", "( •_• )", "( •_• ) 💨",
                "👻 𝖦𝖧𝖮𝖲𝖳 𝖨𝖲 𝖡𝖤𝖧𝖨𝖭𝖣 𝖸𝖮𝖴!", "⌬ 𝖣𝖮𝖭'𝖳 𝖫𝖮𝖮𝖪 𝖡𝖠𝖢𝖪. 🌚"
            ]
            for f in frames: await event.edit(f); await asyncio.sleep(1.2)

        # --- 2. HACK ---
        elif cmd == "hack":
            frames = [
                "⌬ 𝖢𝖮𝖭𝖭𝖤𝖢𝖳𝖨𝖭𝖦 𝖳𝖮 𝖳𝖮𝖱 𝖭𝖤𝖳𝖶𝖮𝖱𝖪... 📡",
                "⌬ 𝖡𝖸𝖯𝖠𝖲𝖲𝖨𝖭𝖦 𝟤𝖥𝖠 𝖲𝖧𝖨𝖤𝖫𝖣... [𝖣𝖮𝖭𝖤] 🛡️",
                "⌬ 𝖨𝖭𝖩𝖤𝖢𝖳𝖨𝖭𝖦 𝖲𝖰𝖫 𝖯𝖠𝖸𝖫𝖮𝖠𝖣... 💾",
                "⌬ 𝖴𝖯𝖫𝖮𝖠𝖣𝖨𝖭𝖦 𝖳𝖮 𝖬𝖠𝖨𝖭𝖥𝖱𝖠𝖬𝖤... 𝟫𝟫% ⚙️",
                "⌬ 𝖲𝖸𝖲▵▤𝖬 𝖧𝖠𝖢𝖪𝖤𝖣 𝖡𝖸 𝖬𝖲𝖣. 💀"
            ]
            for f in frames: await event.edit(f); await asyncio.sleep(1.3)

        # --- 3. NUKE ---
        elif cmd == "nuke":
            frames = [
                "🔴 𝖲𝖸𝖲𝖳𝖤𝖬: 𝖭𝖴𝖪𝖤 𝖠𝖴𝖳𝖧𝖮𝖱𝖨𝖹𝖤𝖣.", "🚀 𝖨𝖢𝖡𝖬 𝖫𝖠𝖴𝖭𝖢𝖧𝖤𝖣...",
                "🛰️ 𝖳𝖱𝖠𝖩𝖤𝖢𝖳𝖮𝖱𝖸: 𝖲𝖤𝖳", "⌬ 𝖨𝖬𝖯𝖠𝖢𝖳 𝖨𝖭: 𝟥... 𝟤... 𝟣...",
                "💥 𝖡 𝖮 𝖮 𝖮 𝖮 𝖬 𝖬 𝖬 𝖬 !!!", "░░░░░░███████ ]▄▄▄▄▄▄▄▄",
                "🏁 𝖹𝖮𝖭𝖤: 𝖣𝖤𝖠𝖣. 𝖱𝖠𝖣𝖨𝖠𝖳𝖨𝖮𝖭: 𝟣𝟢𝟢% ☢️"
            ]
            for f in frames: await event.edit(f); await asyncio.sleep(1.1)

        # --- 4. EXTREME: HORNY ---
        elif cmd == "horny":
            frames = [
                "⌬ 𝖲𝖸𝖲𝖳𝖤𝖬 𝖳𝖤𝖬𝖯𝖤𝖱𝖠𝖳𝖴𝖱𝖤: 𝖱𝖨𝖲𝖨𝖭𝖦... 🔥",
                "⌬ 𝖵𝖨𝖡𝖱𝖠𝖳𝖨𝖮𝖭𝖲 𝖲𝖤𝖳 𝖳𝖮 𝖴𝖫𝖳𝖱𝖠 ⚡",
                "⌬ 𝖧𝖠𝖱𝖣𝖤𝖱... 𝖥𝖠𝖲𝖳𝖤𝖱... 𝖡𝖤𝖳𝖳𝖤𝖱. 🌀",
                "⌬ 𝖡𝖫𝖮𝖮𝖣 𝖯𝖴𝖬𝖯𝖨𝖭𝖦: 𝖬𝖠𝖷𝖨𝖬𝖴𝖬 🩸",
                "⌬ 𝖢𝖠𝖭 𝖸𝖮𝖴 𝖧𝖠𝖭𝖣𝖫𝖤 𝖳𝖧𝖨𝖲 𝖧𝖤𝖠𝖳? 🥵",
                "💦 𝖤 𝖷 𝖯 𝖫 𝖮 𝖣 𝖤 𝖣 ! ! !", "⌬ 𝖲𝖸𝖲𝖳𝖤𝖬 𝖮𝖵𝖤𝖱𝖫𝖮𝖠𝖣𝖤𝖣. 🤤"
            ]
            for f in frames: await event.edit(f); await asyncio.sleep(1.2)

        # --- 5. MOVIE: DINO ---
        elif cmd == "dino":
            frames = [
                "🏃💨💨 (TEZI SE!)\n/ \\\n\"Bhaago!\"",
                "🏃💨     🦖 (AA GAYA!)\n/ \\     / \\\n       (BHAYANAK!)",
                "🚧 (DEEWAR!) 🏃\n            |  | 🦖🔥🔥\n            |__| / \\\n            (FAS GAYA!)",
                " 🏃 (EPIC KUDO!)\n  ⬇️  🦖🔥\n     / \\ (HATH NAHIN AAYAA!)",
                "🏃 🍕 🦖 (DINO PIZZA LAAYAA?)\n/ \\  / \\\n(SWAP!)",
                "😋 (KHANA CHALU!)\n/ \\ 🦖💤 (DINO SO GAYA)\n/ \\ / \\\n(MAZAA AA GAYA!)"
            ]
            for f in frames: await event.edit(f); await asyncio.sleep(1.5)

        # --- 6. MOVIE: FLY ---
        elif cmd == "fly":
            frames = [
                "🔭︻┳デ═—  🪰 (NISHANA!)\n( -_-)",
                "🔭︻┳デ═— 💨 (GAI!)\n( >_<)   🪰 💨 (BACH GAI!)",
                "( O_O)   💨🪰\n(____) (AA RAHI HAI!)\n(OOPS!)",
                "( >д<) 👋 🪰\n /  \\    (KAAT RAHI HAI!)\n(DARD!)",
                "( @ _@)  🪰 (WIN!)\n(____)\n(HAAR GAYA!)",
                "🏃💨💨💨   🪰💨\n(NIKAL LO!)"
            ]
            for f in frames: await event.edit(f); await asyncio.sleep(1.5)

        # --- 7. MOVIE: UFO ---
        elif cmd == "ufo":
            frames = [
                "☁️ (KHALI KHET)\n  🐄 (KHALI MAUJA)\n🌿🌿🌿",
                " 🛸 (VOOM!)\n(YE KYA?) 🐄\n🌿🌿🌿",
                " 🛸\n|✨| (UPAR CHAL!)\n|🐄| (NAHIN!)\n🌿🌿🌿",
                " 🛸 (GULP!)\n 🌿🌿🌿 (POORA GAYA!)",
                " 🛸 (NUKSAAN!)\n|✨| ⬇️ (BAHAR CHAL!)\n  🐄 (ZOR SE GIRA!)\n🌿🌿🌿",
                "🛸💨 (BHAG GAYA!)\n   🐄🕶️ (ALAG SWAG!)\n🌿🌿🌿 (SWAG DEKH!)"
            ]
            for f in frames: await event.edit(f); await asyncio.sleep(1.5)

        # --- 8. MOVIE: LIFT ---
        elif cmd == "lift":
            frames = [
                "🏋️‍♂️ (HATHI VAZAN!)\n 🦴 (DUBRA)\n\"Uttha Lunga!\"",
                "🏋️‍♂️\n😖 (DAMM LAGA!)\n/ \\\n(DAMN!)",
                "🏋️‍♂️ 🆙\n😫 (BAS HOGYA!)\n/ \\\n(AAGYAA!)",
                "⬇️ (GIR GAYAA!)\n😱 (ABBE!)\n🏋️‍♂️",
                "😵 (DABB GAYA!)\n🏋️‍♂️ (BACHAO!)",
                "🤕 (POORA TUTT GAYA!)\n/ \\  🏋️‍♂️"
            ]
            for f in frames: await event.edit(f); await asyncio.sleep(1.5)

        # --- 9. MOVIE: FIGHT ---
        elif cmd == "fight":
            frames = [
                "🤠 (Khabardar!)\n<)  )>  vs  😎 (Kya re?)\n /  \\      <)  )╯\n            /  \\",
                "          😎\nGOLI!! 💨💨 🔫🤠\n      💨  <)  )>\n         /  \\",
                "      Oww!\n__😎__   🔫🤠\n(______)   / \\\n(OHH TERI!)",
                "          🤠 (Nikal Gayi?)\n💨 💨💨 💨 / \\\n__😎__   \n(MISS!)",
                "😎\n<)  )╯  <-- 🤠 (Hain?)\n /  \\      <)  )>\n            /  \\",
                "😎 (KHATAM!)\n<)  )╯ 💥🔫🤠💤\n /  \\  (BETA GAYE!)"
            ]
            for f in frames: await event.edit(f); await asyncio.sleep(1.5)

        # --- 10. MOVIE: BOTTLE ---
        elif cmd == "bottle":
            frames = [
                "🥤 (Bottle)\n(⌐■_■) 🧔\n\"Dekho mera kamaal!\"",
                "🔄🥤 (Hawa mein!)\n🧔 (Confidence!)",
                "✨ 🥤 ✨ (Seedhi giregi?)\n🧔 (Eyes closed)",
                "💥🥤💥 (Sar par giri!)\n( >_<)\n\"AAIYYOOO!\"",
                "💦🧔💦 (Geela ho gaya)\n( -_-)\n\"Bohot badiya!\"",
                "🚶‍♂️💨 (Sharam se bhaga)\n🥤 (Bottle has rahi hai)"
            ]
            for f in frames: await event.edit(f); await asyncio.sleep(1.5)

        # --- 11. MOVIE: PRO ---
        elif cmd == "pro":
            frames = [
                "🔭︻┳デ═— 👤 (Dushman)\n( -_-)\n\"Khatam hai tu!\"",
                "🔥︻┳デ═— 💨 (DISHKYAAO!)\n( >_<) ",
                "💨 💨  🍌 (Kela gira!)\n🔭     👤",
                "💨 🍌 💥 (Bullet slip ho gayi!)\n🔭 (What??)\n👤 (Bach gaya!)",
                "🔭      🔫👤 (Usne dekh liya!)\n( 😱)  \"Abbe teri...!\"",
                "🏃💨💨💨 🔫👤💨\n(Ulta bhaagna pada!)"
            ]
            for f in frames: await event.edit(f); await asyncio.sleep(1.5)

        # --- 12. MOVIE: PROPOSE ---
        elif cmd == "propose":
            frames = [
                "🤵 💐 (Gulaab leke)\n( ^_^)\n\"Aaj 'Haan' bolegi!\"",
                "      💐\n     (  -_- ) 💍 (Ring!)\n     /  |_\n\"Pyaar karta hoon!\"",
                "🏃‍♀️💨 (Tezi se aayi)\n( O_O)\n🤵 (Umeed jagi!)",
                "🏃‍♀️💨💨 🍕\n(Pizza wala piche tha!)\n🤵 (Akele khada hai)",
                "🤵 🥀 (Phool murjha gaye)\n( T_T)\n\"Kismat hi tati hai!\"",
                "🐕 (Kutta phool le gaya)\n🤵 (Khali hath!)"
            ]
            for f in frames: await event.edit(f); await asyncio.sleep(1.5)

        # --- 13. MOVIE: HERO ---
        elif cmd == "hero":
            frames = [
                "☁️    🦸‍♂️ (I AM FLYING!)\n       /  \\\n    \"Duniya bachaunga!\"",
                "☁️    🦸‍♂️ (Wait...)\n        ( >_<)\n    \"A... A... A...\"",
                "💥💨 🦸‍♂️ 🤧 (AA-CHOOO!)\n🚀 (Piche se rocket speed!)\n    \"BHOOOOM!\"",
                "🌀🌀 🦸‍♂️ 🌀🌀\n    (Dizzy!)\n    \"Roko re baba!\"",
                "🏙️\n    💥💥💥 (Building mein ghusa)\n    🦸‍♂️ (Sir bahar, baki andar)",
                "🤕 (Patti bandhi hai)\n    \"Allergy ne maar diya!\""
            ]
            for f in frames: await event.edit(f); await asyncio.sleep(1.5)

        # --- 14. MOVIE: NASA ---
        elif cmd == "nasa":
            frames = [
                "💻 (NASA HACKING...)\n⌨️ 👨‍💻 (Ungliyan tezi se!)\n\"Aaj toh system hang!\"",
                "⚡ ✨ ⚡\n< CODE LOADING... >\n👨‍💻 (Chashma lagaya!)",
                "99%... 🟢\n👨‍💻 (Khushi ke aansu!)\n\"Bas hone wala hai!\"",
                "🌑 (ANDHERA!)\n(O_O) \"Ae bhai??\"\n🔌 (Wire nikal gaya!)",
                "🕯️ (MOM-BATTI)\n😭 (Kismat kharab!)\n\"Poora mehnat paani mein!\"",
                "💤 💻 (Laptop dead)\n\"Chalo so jaate hain!\""
            ]
            for f in frames: await event.edit(f); await asyncio.sleep(1.5)

        # --- 15. EXTREME: BDSM ---
        elif cmd == "bdsm":
            frames = [
                "⌬ 𝖢𝖧𝖠𝖨𝖭𝖲 𝖴𝖭𝖫𝖮𝖢𝖪𝖤𝖣... ⛓️", "🧎 𝖪𝖭𝖤𝖤𝖫. 𝖣𝖮𝖭'𝖳 𝖬𝖠𝖪𝖤 𝖬𝖤 𝖠𝖲𝖪 𝖳𝖶𝖨𝖢𝖤.",
                "⌬ 𝖳𝖨𝖦𝖧𝖳𝖤𝖭𝖨𝖭𝖦 𝖳𝖧𝖤 𝖢𝖮𝖫𝖫𝖠𝖱... 🩸", "⌬ 𝖥𝖤𝖤𝖫 𝖳𝖧𝖤 𝖶𝖧𝖨𝖯 𝖮𝖭 𝖸𝖮𝖴𝖱 𝖲𝖪𝖨𝖭. ⛓️",
                "⌬ 𝖯𝖠𝖨𝖭 𝖨𝖲 𝖯𝖫𝖤𝖠𝖲𝖴𝖱𝖤 𝖧𝖤𝖱𝖤... 👑", "💀 𝖲𝖨𝖫𝖤𝖭𝖢𝖤 𝖨𝖲 𝖸𝖮𝖴𝖱 𝖮𝖭𝖫𝖸 𝖲𝖠𝖥𝖤 𝖶𝖮𝖱𝖣.", "⌬ 𝖮𝖡𝖤𝖸 𝖳𝖧𝖤 𝖬𝖠𝖲𝖳𝖤𝖱. 👑"
            ]
            for f in frames: await event.edit(f); await asyncio.sleep(1.2)

        # --- 16. STRIP ---
        elif cmd == "strip":
            frames = [
                "🧥 (Coat Off)", "👕 (Shirt Off)", "👖 (Pants Off)", "👙 (Underwear)",
                "🔞 𝖥𝖴𝖫𝖫 𝖲𝖳𝖱𝖨𝖯𝖯𝖤𝖣.", "⌬ 𝖤𝖭𝖩𝖮𝖸 𝖳𝖧𝖤 𝖵𝖨𝖤𝖶."
            ]
            for f in frames: await event.edit(f); await asyncio.sleep(1.2)

        # --- ADDITIONAL SETS ---
        elif cmd == "blow":
            frames = ["⌬ 𝖯𝖱𝖤𝖯𝖠𝖱𝖨𝖭𝖦... 👅", "𝟪=𝖣", "𝟪==𝖣", "𝟪===𝖣", "𝟪====𝖣", "𝟪=====𝖣 💦👅", "⌬ 𝖳𝖧𝖠𝖳 𝖶𝖠𝖲 𝖣𝖤𝖤𝖯. 🥵"]
            for f in frames: await event.edit(f); await asyncio.sleep(1.1)

        elif cmd == "cum":
            frames = ["𝟪=𝖣", "𝟪=𝖣💦", "𝟪=𝖣 💦 💦", "𝟪=𝖣  💦  💦  💦", "⌬ 𝖬𝖤𝖲𝖲𝖸 𝖥𝖨𝖭𝖨𝖲𝖧. 🍼"]
            for f in frames: await event.edit(f); await asyncio.sleep(1.1)

        elif cmd == "pounding":
            frames = ["εつ💦(‿ˠ‿) (Push...)", "εつ🔥(‿ˠ‿) (Harder!)", "εつ🌊(‿ˠ‿) (Deep!)", "⌬ 𝖱𝖧𝖸𝖳𝖧𝖬 𝖫𝖮𝖢𝖪𝖤𝖣. ⚡"]
            for f in frames: await event.edit(f); await asyncio.sleep(0.9)

        elif cmd == "sex":
            frames = ["🍆", "🍑", "👉", "👌", "⚡", "🔥", "💦", "💥", "⌬ 𝖯𝖴𝖱𝖤 𝖧𝖤𝖠𝖳. 🔞"]
            for f in frames: await event.edit(f); await asyncio.sleep(1.0)

        elif cmd == "climax":
            frames = ["( . Y . )", "🥛", "🤤 𝖣𝖮𝖭𝖤!", "⌬ 𝖯𝖮𝖶𝖤𝖱 𝖮𝖥𝖥. 🔌"]
            for f in frames: await event.edit(f); await asyncio.sleep(1.2)

        elif cmd == "brain":
            res = ["100% Psycho Detected", "Genius Mind", "Pure Evil", "Master of Shadows", "No Brain Found"]
            await event.edit("⌬ 𝖲𝖢𝖠𝖭𝖭𝖨𝖭𝖦 𝖡𝖱𝖠𝖨𝖭... 🧠"); await asyncio.sleep(1.5)
            await event.edit(f"⌬ 𝖱𝖤𝖲𝖴𝖫𝖳: [{random.choice(res)}] 💀")

        elif cmd == "toss":
            res = ["HEADS 🪙", "TAILS 🪙"]
            await event.edit("🌪️ 𝖥𝖫𝖨𝖯𝖯𝖨𝖭𝖦..."); await asyncio.sleep(1.5)
            await event.edit(f"⌬ 𝖱𝖤𝖲𝖴𝖫𝖳: [{random.choice(res)}]")

    except Exception as e:
        print(f"Animation Error: {e}")

# --- 3. SETUP ---
async def setup(client):
    client.add_event_handler(anim_help)
    client.add_event_handler(master_anim_handler)
                
