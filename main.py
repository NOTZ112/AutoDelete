#=========================================================================
# [AutoDelete - Telegram bot to delete messages after specific time]      
# Copyright (C) 2022 Arunkumar Shibu                       
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#=========================================================================

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


@User.on_message(filters.group)
async def auto_delete_handler(client, message: Message):
    settings = get_group(message.chat.id)

    if not settings:
        return

    if not settings.get("enabled", False):
        return

    if message.service:
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
    await message.reply_text(
        "✅ Auto Delete Enabled"
    )


@User.on_message(filters.command("disable") & filters.group)
async def disable_cmd(client, message: Message):
    disable_group(message.chat.id)
    await message.reply_text(
        "❌ Auto Delete Disabled"
    )


@User.on_message(filters.command("settime") & filters.group)
async def settime_cmd(client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "Usage:\n/settime 60"
        )

    try:
        sec = int(message.command[1])
    except:
        return await message.reply_text(
            "Please enter only numbers."
        )

    set_group_time(
        message.chat.id,
        sec
    )

    await message.reply_text(
        f"✅ Delete Time Updated\n\n{sec} Seconds"
    )


@User.on_message(filters.command("status") & filters.group)
async def status_cmd(client, message: Message):
    data = get_group(message.chat.id)

    if not data:
        return await message.reply_text(
            "❌ Auto Delete Disabled"
        )

    status = "ON" if data.get("enabled") else "OFF"

    await message.reply_text(
        f"
