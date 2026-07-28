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
        {"chat_id": chat_id},
        {"$set": {"enabled": False}},
        upsert=True
    )


def set_group_time(chat_id, seconds):
    groups.update_one(
        {"chat_id": chat_id},
        {"$set": {"time": seconds}},
        upsert=True
    )
