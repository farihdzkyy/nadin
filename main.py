import asyncio
from pyrogram import Client, filters
import json

# Replace with your credentials
api_id = '2374504'
api_hash = '2ea965cd0674f1663ec291313edcd333'

app = Client("my_account", api_id=api_id, api_hash=api_hash)

# Store allowed users in a JSON file
ALLOWED_USERS_FILE = "allowed_users.json"

def load_allowed_users():
    try:
        with open(ALLOWED_USERS_FILE, 'r') as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_allowed_users(users):
    with open(ALLOWED_USERS_FILE, 'w') as f:
        json.dump(list(users), f)

allowed_users = load_allowed_users()

@app.on_message(filters.command("add", prefixes=".") & filters.reply)
async def add_user(client, message):
    if message.from_user.id != 1896544984:  # Replace YOUR_ADMIN_ID with your actual user ID
        await message.reply_text("You're not authorized to add users.")
        return
    
    replied_user = message.reply_to_message.from_user.id
    allowed_users.add(replied_user)
    save_allowed_users(allowed_users)
    await message.reply_text(f"User {replied_user} added to allowed users.")

@app.on_message(filters.command("sp", prefixes=".") & filters.reply)
async def delayspam(client, message):
    if message.from_user.id not in allowed_users:
        await message.reply_text("You're not authorized to use this command.")
        return

    try:
        # Extract the arguments from the command
        args = message.text.split()
        if len(args) < 4:
            await message.reply_text("Format tidak valid. Gunakan format: .sp (@nama_grup1) (@nama_grup2) ... (waktu_delay) (batas_pesan)")
            return
        
        # Extract group names, delay, and limit
        group_names = args[1:-2]
        delay = int(args[-2])
        limit = int(args[-1])
        
        if len(group_names) < 1 or len(group_names) > 10:
            await message.reply_text("Jumlah grup minimal 1 dan maksimal 10.")
            return
        
        # Get the message to be forwarded
        spam_message = message.reply_to_message
        
        # Forward the message with the specified delay and limit to each group
        for group in group_names:
            for _ in range(limit):
                await spam_message.forward(group)
                await asyncio.sleep(delay)
        
        await message.reply_text("Spam selesai.")
        
    except Exception as e:
        await message.reply_text(f"Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
