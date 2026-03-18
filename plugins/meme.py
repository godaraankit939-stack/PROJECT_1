import random
import requests
from telethon import events

# ================= CONFIG =================

TENOR_API_KEY = "LIVDSRZULELA"

# 🔥 👉 TERE PURE DESI SOURCES (EXPANDED)
SEARCH_TERMS = [

# 🎬 MOVIES
"hera pheri babu rao meme",
"phir hera pheri meme",
"welcome nana patekar meme",
"welcome uday control meme",
"gangs of wasseypur meme",
"munna bhai meme jadoo ki jhappi",
"golmaal vasooli bhai meme",
"3 idiots all is well meme",
"dhamaal sanjay mishra meme",
"ms dhoni movie meme",
"lagaan meme kachra",
"bajirao mastani meme ranveer singh",
"singham aata majhi satakli meme",
"gunda mithun meme",

# 📺 WEB SERIES
"mirzapur kaleen bhaiya meme",
"mirzapur munna bhaiya meme",
"sacred games gaitonde meme",
"family man chellam sir meme",
"panchayat binod meme",
"scam 1992 harshad mehta meme",
"shark tank ashneer meme",

# 🎥 YOUTUBERS
"carryminati meme",
"bb ki vines titu mama meme",
"ashish chanchlani meme",
"triggered insaan meme",
"flying beast meme",
"hindustani bhau meme",
"puneet superstar meme",
"technical guruji meme",
"sandeep maheshwari meme",

# 👤 PERSONALITIES
"narendra modi mitron meme",
"rahul gandhi meme funny",
"arvind kejriwal meme",
"kamlesh soluchan meme",
"aamir khan interview meme",
"shashi tharoor english meme",

# 📺 TV SHOWS
"tmkoc jethalal meme",
"tmkoc daya meme",
"cid daya darwaza tod do meme",
"crime patrol meme",
"rasode mein kaun tha meme",
"koffee with karan meme"
]

REDDIT_SUBS = [
    "IndianDankMemes",
    "dankinindia"
]

# ================= TENOR =================

def get_tenor():
    try:
        query = random.choice(SEARCH_TERMS)
        url = f"https://tenor.googleapis.com/v2/search?q={query}&key={TENOR_API_KEY}&limit=20"

        res = requests.get(url, timeout=5).json()
        results = res.get("results", [])

        if results:
            gif = random.choice(results)
            return gif["media_formats"]["gif"]["url"]

    except:
        pass
    return None

# ================= REDDIT =================

def get_reddit():
    try:
        sub = random.choice(REDDIT_SUBS)
        url = f"https://meme-api.com/gimme/{sub}"

        res = requests.get(url, timeout=5).json()

        if res and "url" in res:
            return res["url"]

    except:
        pass
    return None

# ================= COMMAND =================

@events.register(events.NewMessage(pattern=r"\.meme"))
async def meme(event):
    await event.edit("`🔥 Desi Meme aa raha hai...`")

    # 🔥 1st priority → Tenor (your categories)
    meme = get_tenor()

    # 🔥 fallback → Reddit
    if not meme:
        meme = get_reddit()

    if meme:
        await event.delete()
        return await event.client.send_file(event.chat_id, meme)

    await event.edit("❌ Meme nahi mila")

# ================= SETUP =================

async def setup(client):
    client.add_event_handler(meme)
