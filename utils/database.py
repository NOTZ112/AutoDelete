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

from .info import DATABASE_URI
from pymongo import MongoClient

dbclient = MongoClient(DATABASE_URI)

db = dbclient["AutoDelete"]

messages = db["MESSAGES"]
groups = db["GROUPS"]


# ---------------- Messages ---------------- #

def save_message(chat_id, message_id, delete_time):
    messages.insert_one({
        "chat_id": chat_id,
        "message_id": message_id,
        "time": delete_time
    })


def get_all_data(current_time):
    return list(messages.find({
        "time": {
            "$lte": current_time
        }
    }))


def delete_all_data(all_data):
    for data in all_data:
        messages.delete_one({
            "_id": data["_id"]
        })


# ---------------- Groups ---------------- #

def get_group(chat_id):
    return groups.find_one({
        "chat_id": chat_id
    })



    else:
        groups.insert_one({
            "chat_id": chat_id,
            "enabled": True,
            "time": 10
        })
        },
        upsert=True
    )
def enable_group(chat_id):
    group = get_group(chat_id)

    if group:
        groups.update_one(
            {"chat_id": chat_id},
            {"$set": {"enabled": True}}
        )
    else:
        groups.insert_one({
            "chat_id": chat_id,
            "enabled": True,
            "time": 10
        })

def disable_group(chat_id):
    groups.update_one(
        {
            "chat_id": chat_id
        },
        {
            "$set": {
                "enabled": False
            }
        },
        upsert=True
    )


def set_group_time(chat_id, seconds):
    groups.update_one(
        {
            "chat_id": chat_id
        },
        {
            "$set": {
                "time": seconds
            }
        },
        upsert=True
    )
