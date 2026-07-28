from time import time
from subprocess import Popen

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.info import *
from utils.database import *

User = Client(
    "auto-delete-user",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION
)


@User.on_message(filters.group & ~filters.service)
async def auto_delete_handler(client, message: Message):
    settings = get_group(message.chat.id)

    if not settings:
        return

    if not settings.get("enabled", False):
        return

    delete_after = settings.get("time", 10)

    save_message(
        chat_id=message.chat.id,
        message_id=message.id,
        delete_time=int(time()) + delete_after
    )


@User.on_message(filters.command("enable") & filters.group)
async def enable_cmd(client, message: Message):
    enable_group(message.chat.id)
    await message.reply_text("✅ Auto Delete Enabled")


@User.on_message(filters.command("disable") & filters.group)
async def disable_cmd(client, message: Message):
    disable_group(message.chat.id)
    await message.reply_text("❌ Auto Delete Disabled")
    @User.on_message(filters.command("status") & filters.group)
async def status_cmd(client, message: Message):
    data = get_group(message.chat.id)

    if not data:
        return await message.reply_text(
            "❌ Auto Delete Disabled"
        )

    status = "ON" if data.get("enabled", False) else "OFF"

    await message.reply_text(
        f"📊 Status: {status}\n"
        f"⏱ Delete Time: {data.get('time', 10)} Seconds"
    )


@User.on_message(filters.command("settime") & filters.group)
async def settime_cmd(client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "Usage:\n/settime 60"
        )

    try:
        sec = int(message.command[1])
    except ValueError:
        return await message.reply_text(
            "❌ Please enter only numbers."
        )

    set_group_time(message.chat.id, sec)

    await message.reply_text(
        f"✅ Delete Time Updated to {sec} Seconds"
    )


@User.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message: Message):
    await message.reply_text(
        "**✅ Multi Group Auto Delete UserBot Running**\n\n"
        "Commands:\n"
        "/enable\n"
        "/disable\n"
        "/settime 60\n"
        "/status"
    )


Popen(
    f"gunicorn utils.server:app --bind 0.0.0.0:{PORT}",
    shell=True
)

Popen(
    "python3 -m utils.delete",
    shell=True
)

print("✅ Multi Group Auto Delete Started")

User.run()
