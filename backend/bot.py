from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
import asyncio
import requests
import json
import os

API_TOKEN = ''
BACKEND_URL = 'http://127.0.0.1:5000/api/users'
JSON_FILE = 'users.json'

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

def load_users():
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_users(users):
    with open(JSON_FILE, 'w') as file:
        json.dump(users, file, indent=4)

@dp.message(Command("start"))
async def start_bot(message: Message):
    users = load_users()
    new_user_id = 1 if not users else max(user["userId"] for user in users) + 1
    new_user = {
        "userId": new_user_id,
        "objects": [
            { "name": "apple", "count": 0 },
            { "name": "banana", "count": 0 },
            { "name": "soup", "count": 0 },
            { "name": "carrot", "count": 0 },
            { "name": "Scrooge coin", "count": 0 }
        ]
    }

    users.append(new_user)

    save_users(users)

    await message.reply(
        f"Welcome! You have been registered as User ID {new_user_id}.\n"
        f"Your initial object counts are:\n"
        f"- Apple: 0\n"
        f"- Banana: 0\n"
        f"- Soup: 0\n"
        f"- Carrot: 0\n"
        f"- Scrooge coin: 0"
    )

@dp.message(Command("buy"))
async def buy_object(message: Message):
    args = message.text.split()
    if len(args) != 4:
        await message.reply("Usage: /buy <user_id> <object_name> <count>")
        return

    user_id, object_name, count = args[1], args[2], args[3]
    payload = {
        "action": "buy",
        "name": object_name,
        "count": int(count)
    }

    response = requests.post(f"{BACKEND_URL}/{user_id}/objects", json=payload)
    if response.status_code == 200:
        await message.reply(f"Bought {count} {object_name}(s).")
    else:
        await message.reply(f"Error: {response.json().get('error')}")

@dp.message(Command("sell"))
async def sell_object(message: Message):
    args = message.text.split()
    if len(args) != 4:
        await message.reply("Usage: /sell <user_id> <object_name> <count>")
        return

    user_id, object_name, count = args[1], args[2], args[3]
    payload = {
        "action": "sell",
        "name": object_name,
        "count": int(count)
    }

    response = requests.post(f"{BACKEND_URL}/{user_id}/objects", json=payload)
    if response.status_code == 200:
        await message.reply(f"Sold {count} {object_name}(s).")
    else:
        await message.reply(f"Error: {response.json().get('error')}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
