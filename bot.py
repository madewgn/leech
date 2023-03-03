import os
from requests import delete, patch
from pyrogram import Client, filters
import main
from pyrogram.types import User, Message
from pySmartDL import SmartDL


DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./download/")

bughunter0 = Client(
    "leech",
    bot_token="5081813572:AAFhTV5vD9XEjmC4qPkBw0YTkmm5ZJlVbnw",
    api_id="2345226",
    api_hash="6cc6449dcef22f608af2cf7efb76c99d"
)


@bughunter0.on_message(filters.command(["start"]))
async def start(bot, message):
    txt = await message.reply_text("halo")


@bughunter0.on_message(filters.command(["pull"]))
async def pull(bot, message):
    txt = await message.reply_text("updating...")
    os.system("git pull")


@bughunter0.on_message(filters.text & filters.private)
async def leech(bot, message):
    text = str(message.text)
    chat_id = int(message.chat.id)
    link = main.get_link(text)

    # download video
    txt = await message.reply_text("Downloading to My server.....")
    obj = SmartDL(link, DOWNLOAD_LOCATION)
    dl = obj.start()
    path = obj.get_dest()
    tub = main.create_thumbnail(path)
    imfo = main.with_moviepy(path)
    durasi = imfo[0]
    fps = imfo[1]
    width = imfo[2]
    height = imfo[3]
#    await txt.edit_text("uploading....")
    await txt.delete()
    print("uploading")
    # convert to audio
    await message.reply_video(video=path, supports_streaming=True, thumb=tub, caption=path, height=int(height), width=int(width), duration=int(durasi))

    # remove file
    try:
        os.remove(path)
        os.remove(tub)
    except:
        pass


print("aktif")
bughunter0.run()

