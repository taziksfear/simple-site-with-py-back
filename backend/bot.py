from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
import asyncio
import requests
import json
import os

# Replace with your bot token
API_TOKEN = ''
BACKEND_URL = 'http://127.0.0.1:5000/api/users'  # Flask backend URL
JSON_FILE = 'users.json'  # Path to the JSON file

# Initialize bot with default properties
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)  # Set default parse mode
)
dp = Dispatcher()

# Function to load users from JSON file
def load_users():
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

# Function to save users to JSON file
def save_users(users):
    with open(JSON_FILE, 'w') as file:
        json.dump(users, file, indent=4)

# Command to start the bot and create a new user
@dp.message(Command("start"))
async def start_bot(message: Message):
    # Load existing users
    users = load_users()

    # Generate a new user ID
    new_user_id = 1 if not users else max(user["userId"] for user in users) + 1

    # Create a new user with default object counts
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

    # Add the new user to the list
    users.append(new_user)

    # Save the updated list to the JSON file
    save_users(users)

    # Send a welcome message to the user
    await message.reply(
        f"Welcome! You have been registered as User ID {new_user_id}.\n"
        f"Your initial object counts are:\n"
        f"- Apple: 0\n"
        f"- Banana: 0\n"
        f"- Soup: 0\n"
        f"- Carrot: 0\n"
        f"- Scrooge coin: 0"
    )

# Command to buy objects
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

    # Send request to backend
    response = requests.post(f"{BACKEND_URL}/{user_id}/objects", json=payload)
    if response.status_code == 200:
        await message.reply(f"Bought {count} {object_name}(s).")
    else:
        await message.reply(f"Error: {response.json().get('error')}")

# Command to sell objects
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

    # Send request to backend
    response = requests.post(f"{BACKEND_URL}/{user_id}/objects", json=payload)
    if response.status_code == 200:
        await message.reply(f"Sold {count} {object_name}(s).")
    else:
        await message.reply(f"Error: {response.json().get('error')}")

# Start the bot
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
