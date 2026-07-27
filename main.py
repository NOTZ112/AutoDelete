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
