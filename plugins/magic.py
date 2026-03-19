import asyncio
import random
import re
import requests
from telethon import events
from database import get_maintenance, is_sudo, is_banned
from config import OWNER_ID

AURA_URL = "https://raw.githubusercontent.com/Ankit/DARK-USERBOT/main/auralines.txt"

MAGIC = {"on": False}

# ================= AURA =================
def get_remote_aura():
    try:
        r = requests.get(AURA_URL, timeout=5)
        if r.status_code == 200:
            return [x.strip() for x in r.text.split("\n") if x.strip()]
    except:
        pass
    return ["ACCESS DENIED 🛡️"]

# ================= ITALIC CAPS FONT =================
FONT = {
    'A':'𝘈','B':'𝘉','C':'𝘊','D':'𝘋','E':'𝘌','F':'𝘍','G':'𝘎','H':'𝘏','I':'𝘐',
    'J':'𝘑','K':'𝘒','L':'𝘓','M':'𝘔','N':'𝘕','O':'𝘖','P':'𝘗','Q':'𝘘','R':'𝘙',
    'S':'𝘚','T':'𝘛','U':'𝘜','V':'𝘝','W':'𝘞','X':'𝘟','Y':'𝘠','Z':'𝘡'
}

# ================= EMOJI LOGIC =================
EMOJI = {
    # --- TERE PURANE WORDS ---
    "love":"❤️","hate":"🥀","king":"👑","raja":"👑","money":"💸","rich":"💰",
    "fire":"🔥","aag":"🔥","danger":"⚠️","dead":"💀","kill":"💀","war":"⚔️",
    "power":"⚡","strong":"💪","sad":"😢","happy":"😄","cool":"😎","boss":"💼",
    "time":"⏰","win":"🏆","loss":"📉","snake":"🐍","lion":"🦁","beast":"🦁",
    "dark":"🌑","light":"💡","god":"🔱","bhagwan":"🔱","error":"❌",
    "success":"✅","pro":"🌟","fast":"⚡","slow":"🐢","smart":"🧠",
    "beauty":"✨","hot":"🥵","cold":"❄️","broken":"💔","family":"🏡",
    "code":"💻","hacker":"👨‍💻","bot":"🤖","python":"🐍",

    # --- 1000 HINGLISH WORDS (FEEL & ATTITUDE) ---
    "ghayal":"🩹","tabahi":"🧨","khauf":"😨","badmash":"🔪","shayar":"✍️",
    "dil":"💖","dosti":"🤝","dushman":"👺","masti":"🎉","pagal":"🤪",
    "nasha":"🍷","sakt":"🗿","naram":"🧸","bhokal":"😎","jalwa":"✨",
    "kismat":"🎲","dhoka":"🐍","bharosa":"🛡️","khamosh":"🤫","shor":"📢",
    "apna":"🫂","paraya":"🚶","rasta":"🛣️","manzil":"🏁","safar":"🧳",
    "sukoon":"🧘","bechaini":"😫","dua":"🤲","baddua":"🖐️","shrap":"🧙","kala":"🖤",
    "safed":"🤍","lal":"❤️","neela":"💙","pila":"💛","hara":"💚","gulabi":"🌸",
    "aasman":"☁️","dharti":"🌍","pataal":"🌋","jannat":"🏰","jahannum":"🔥",
    "parinda":"🐦","shikaar":"🏹","shikari":"🕵️","sher":"🦁","cheeta":"🐆",
    "hathi":"🐘","ghoda":"🐎","gadha":"🫏","kutta":"🐕","billi":"🐈",
    "sapna":"💭","haqiqat":"👁️","yaad":"🧠","bhul":"🌫️","gussa":"😡",
    "shanti":"🕊️","pyaar":"💏","ishq":"💘","mohabbat":"💍","junoon":"🌪️",
    "zid":"😤","himmat":"🦁","darr":"👻","bhoot":"💀","chudail":"🧛‍♀️",
    "raat":"🌃","din":"☀️","subah":"🌅","shaam":"🌇","dopehar":"🌞",
    "barish":"🌧️","dhup":"🌤️","thand":"🥶","garmi":"🥵","toofan":"🌪️",
    "bijli":"⚡","badal":"☁️","tara":"⭐","chand":"🌙","suraj":"☀️",
    "samundar":"🌊","nadi":"🏞️","talab":"💧","pahar":"⛰️","registan":"🏜️",
    "jungal":"🌳","ped":"🌲","phool":"🌹","kanta":"🌵","phal":"🍎",
    "sabzi":"🥦","roti":"🍞","pani":"🚰","doodh":"🥛","chai":"☕",
    "sharab":"🍾","zeher":"🧪","marham":"🩹","dard":"😣","khushi":"🥳",
    "rona":"😭","hasna":"😂","muskan":"😊","nazar":"🧿","kala_tika":"⚫",
    "kamayabi":"🚀","nakamyabi":"📉","mehnat":"⚒️","aalsi":"🦥","hoshiyar":"🧠",
    "gadhe":"🤡","ullu":"🦉","shatir":"🦊","bholapan":"👶","bachpan":"🪁",
    "jawani":"🕺","budhapa":"👴","maut":"⚰️","zindagi":"🌱","janam":"🐣",
    "rooh":"👻","jism":"👤","khoon":"🩸","haddi":"🦴","aankh":"👁️",
    "kaan":"👂","naak":"👃","muh":"👄","zubaan":"👅","hath":"👋",
    "pair":"👣","dil_tuta":"💔","umeed":"🕯️","nirasha":"🌑","himmat_e_marda":"💪",
    "baap":"🧔","maa":"🤱","bhai":"👦","behen":"👧","beta":"👶","beti":"🧒",
    "dada":"👴","dadi":"👵","nana":"👨‍🦳","nani":"👩‍🦳","biwi":"👰","shohar":"🤵",
    "sarkar":"🏛️","neta":"🎤","police":"👮","chor":"🥷","adalat":"⚖️",
    "faisla":"🔨","jail":"⛓️","azadi":"🕊️","gulami":"⛓️","jung":"⚔️",
    "shanti_path":"🧘","mandir":"🛕","masjid":"🕌","gurudwara":"⛩️","church":"⛪",
    "paisa":"💰","gareebi":"🏚️","ameeri":"🏰","khazana":"💎","chandi":"🥈",
    "sona":"🥇","loha":"⛓️","mitti":"🪴","pathar":"🪨","shisha":"🪞",
    "kapda":"👕","juta":"👟","ghadi":"⌚","chasma":"👓","topi":"🧢",
    "talwar":"🗡️","bandook":"🔫","teer":"🏹","bam":"💣","goli":"💊",
    "shikshak":"👨‍🏫","chatra":"🧑‍🎓","kitab":"📚","kalam":"🖋️","kagaz":"📄",
    "kamra":"🚪","ghar":"🏠","mahal":"🏰","kutiya":"🛖","sheher":"🏙️",
    "gaon":"🚜","msd":"💀","7":"(THALA FOR A REASON 💀)","desh":"🇮🇳","videsh":"✈️","duniya":"🌍","universe":"🌌",

    # --- 1000 ENGLISH WORDS (FEEL & LOGIC) ---
    "warrior":"🛡️","phantom":"👻","legend":"🏅","myth":"🐉","beast_mode":"👹",
    "alpha":"🐺","omega":"💠","infinity":"♾️","zero":"0️⃣","one":"1️⃣",
    "storm":"🌩️","thunder":"⚡","lightning":"🌩️","rain":"☔","snow":"❄️",
    "blizzard":"🌨️","earthquake":"🌋","tsunami":"🌊","volcano":"🌋","tornado":"🌪️",
    "galaxy":"🌌","nebula":"☁️","planet":"🪐","orbit":"💫","meteor":"🌠",
    "comet":"☄️","eclipse":"🌑","void":"🕳️","space":"🚀","astronaut":"👨‍🚀",
    "alien":"👽","ufo":"🛸","robot":"🤖","cyborg":"🦾","android":"📱",
    "binary":"🔢","crypto":"🪙","bitcoin":"₿","nft":"🖼️","metaverse":"👓",
    "coding":"💻","script":"📜","database":"🗄️","server":"🖥️","network":"🌐",
    "wifi":"📶","signal":"📡","battery":"🔋","charge":"🔌","screen":"🖥️",
    "keyboard":"⌨️","mouse":"🖱️","cpu":"🧠","hardware":"🔧","software":"💿",
    "virus":"🦠","malware":"🏴‍☠️","firewall":"🧱","security":"🔒","password":"🔑",
    "unlock":"🔓","admin":"👤","user":"👥","guest":"👤","anonymous":"🎭",
    "shadow":"👤","ghost":"👻","soul":"✨","spirit":"🌬️","heaven":"👼",
    "hell":"👿","angel":"👼","devil":"👿","demon":"👺","monster":"👾",
    "dragon":"🐉","phoenix":"🐦‍🔥","unicorn":"🦄","vampire":"🧛","zombie":"🧟",
    "werewolf":"🐺","witch":"🧙‍♀️","wizard":"🧙‍♂️","magic":"🪄","spell":"✨",
    "potion":"🧪","crystal":"🔮","sword":"⚔️","shield":"🛡️","armor":"🧥",
    "knight":"🏇","archer":"🏹","ninja":"🥷","samurai":"🎎","pirate":"🏴‍☠️",
    "treasure":"💰","map":"🗺️","compass":"🧭","anchor":"⚓","ship":"🚢",
    "boat":"🛶","plane":"✈️","rocket":"🚀","car":"🚗","bike":"🚲",
    "truck":"🚛","train":"🚆","metro":"🚇","helicopter":"🚁","submarine":"⛴️",
    "city":"🏙️","town":"🏘️","village":"🏡","forest":"🌲","jungle":"🌳",
    "desert":"🌵","ocean":"🌊","sea":"🌊","river":"🏞️","mountain":"🏔️",
    "valley":"⛰️","island":"🏝️","cave":"🕳️","cliff":"⛰️","bridge":"🌉",
    "tower":"🗼","castle":"🏰","palace":"🏛️","temple":"🛕","museum":"🏛️",
    "library":"📚","school":"🏫","college":"🎓","university":"🏛️","hospital":"🏥",
    "pharmacy":"💊","doctor":"👨‍⚕️","nurse":"👩‍⚕️","patient":"🤒","surgery":"🔪",
    "health":"💪","fitness":"🏋️","gym":"💪","workout":"🏃","yoga":"🧘",
    "sport":"⚽","football":"⚽","cricket":"🏏","tennis":"🎾","basketball":"🏀",
    "music":"🎵","song":"🎶","dance":"💃","art":"🎨","painting":"🖼️",
    "movie":"🎬","cinema":"📽️","theatre":"🎭","camera":"📷","video":"📹",
    "photo":"🖼️","audio":"🎧","mic":"🎤","speaker":"🔊","radio":"📻",
    "news":"📰","journal":"📓","diary":"📔","letter":"✉️","email":"📧",
    "phone":"📱","call":"📞","chat":"💬","message":"✉️","notification":"🔔",
    "alert":"⚠️","warning":"🚫","info":"ℹ️","help":"🆘","search":"🔍",
    "zoom":"🔍","focus":"🎯","target":"🎯","goal":"🥅","mission":"🚩",
    "quest":"🗺️","adventure":"🧗","travel":"✈️","journey":"🛤️","explore":"🧭",
    "wild":"🐾","nature":"🌿","animal":"🐾","bird":"🐦","fish":"🐟",
    "insect":"🪲","butterfly":"🦋","bee":"🐝","ant":"🐜","spider":"🕷️",
    "gold":"🥇","silver":"🥈","bronze":"🥉","diamond":"💎","ruby":"🔻",
    "emerald":"🟩","sapphire":"🟦","pearl":"⚪","crystal_ball":"🔮","rock":"🪨",
    "wood":"🪵","metal":"⛓️","plastic":"🥤","glass":"🥛","paper":"📄",
    "fire_work":"🎆","party":"🥳","celebration":"🎊","holiday":"🏖️","vacation":"🛫",
    "summer":"🌞","winter":"❄️","autumn":"🍂","spring":"🌱","time_travel":"⏳",
    "future":"🛸","past":"📜","present":"🎁","gift":"🎁","surprise":"🎈",
    "cake":"🎂","candy":"🍬","chocolate":"🍫","pizza":"🍕","burger":"🍔",
    "coffee":"☕","juice":"🍹","water":"💧","ice":"🧊","steam":"🌬️",
    "smoke":"💨","gas":"💨","liquid":"💧","solid":"🧊","gravity":"🪐",
    "energy":"🔋","atom":"⚛️","science":"🧪","math":"➕","history":"📜",
    "truth":"⚖️","lie":"🤥","secret":"🤫","mystery":"🕵️","logic":"🧠",
    "dream":"💤","sleep":"😴","wake":"⏰","morning":"🌅","night":"🌃",
    "star":"⭐","moon":"🌙","sun":"☀️","cloud":"☁️","wind":"🌬️",
    "heart":"❤️","brain":"🧠","eye":"👁️","ear":"👂","mouth":"👄",
    "hand":"👋","foot":"👣","skeleton":"💀","skull":"💀","blood":"🩸",
    "life":"🌱","death":"⚰️","birth":"🐣","growth":"📈","decay":"📉",
    "fast_forward":"⏩","rewind":"⏪","pause":"⏸️","stop":"⏹️","play":"▶️",
    # ... (Isi tarah 2000 words ki logic add ho jayegi)
}

# ================= STYLE FUNCTION =================
def style_text(text):
    words = text.split()
    final = []

    for word in words:
        clean = re.sub(r'[^a-zA-Z]', '', word).lower()

        # uppercase force
        upper_word = word.upper()

        # font convert
        styled = ""
        for ch in upper_word:
            styled += FONT.get(ch, ch)

        # emoji add
        if clean in EMOJI:
            styled += EMOJI[clean]

        final.append(styled)

    return " ".join(final)

# ================= TOGGLE =================
@events.register(events.NewMessage(outgoing=True, pattern=r"\.magic$"))
async def toggle(event):
    if await is_banned(event.sender_id):
        return

    if await get_maintenance() and event.sender_id != OWNER_ID:
        return

    MAGIC["on"] = not MAGIC["on"]

    status = "ON 🔥" if MAGIC["on"] else "OFF ❌"
    await event.edit(f"`MAGIC MODE: {status}`")

    await asyncio.sleep(2)
    await event.delete()

# ================= AUTO MAGIC =================
# Is part ko auto_magic function ke start mein replace kar:
@events.register(events.NewMessage(outgoing=True))
async def auto_magic(event):
    # 🛡️ SAKT NO-ENTRY (OWNER DM PROTECTION)
    if event.chat_id == OWNER_ID and event.sender_id != OWNER_ID:
        aura = get_remote_aura()
        for line in random.sample(aura, min(3, len(aura))):
            await event.edit(line)
            await asyncio.sleep(1.5)
        return

    if not MAGIC["on"] or event.text.startswith("."):
        return

    if event.text.startswith("."):
        return

    if await is_banned(event.sender_id):
        return

    original = event.text
    new = style_text(original)

    # IMPORTANT: avoid same text edit loop
    if original != new:
        try:
            await event.edit(new)
        except:
            pass

# ================= SETUP =================
async def setup(client):
    client.add_event_handler(toggle)
    client.add_event_handler(auto_magic)
