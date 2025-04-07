from telethon import TelegramClient, events
import os
import re
import subprocess
import aiofiles

# ⚙️ Configuration
API_ID = 123456  # Replace with your App ID
API_HASH = "your_api_hash"  # Replace with your App Hash
PHONE_NUMBER = "+1234567890"  # Replace with your phone number
LOG_PATH = "/path/to/logs"  # Directory to save files
CHANNEL_ID = -123456789  # Channel ID (negative if it's a channel)

# 🔹 Initialize Telegram client
client = TelegramClient("my_session", API_ID, API_HASH)

async def main():
    await client.start(PHONE_NUMBER)


# 📥 Save forwarded files from the channel
@client.on(events.NewMessage(chats=CHANNEL_ID, forwards=True))
async def save_forwarded_file(event):
    if event.message.file:
        original_name = event.message.file.name
        if not original_name:
            return  # Ignore if no name
        parts = original_name.split(" - ")
        if len(parts) < 2 or not parts[1][:-4].isdigit():
            return  # Ignore if format is unexpected

        file_number = parts[1][:-4]  
        new_filename = f"log_{file_number}.txt"
        file_path = os.path.join(LOG_PATH, new_filename)

        # 📢 # Notify user about file saving
        file_size_gb = round(event.message.file.size / (1024**3), 2) 
        await event.reply(f"📂 Saving `{original_name}` ({file_size_gb} GB)... Please wait.")

        await event.message.download_media(file_path)

        await event.reply(f"✅ File saved as `{new_filename}` in {LOG_PATH}")


# 📜 List files and their sizes
@client.on(events.NewMessage(pattern="/files"))
async def list_files(event):
    files = os.listdir(LOG_PATH)
    if not files:
        await event.reply("📁 No files in the directory.")
        return
    
    file_list = []
    for f in files:
        if f.endswith('.txt'):
            file_path = os.path.join(LOG_PATH, f)
            size_gb = os.path.getsize(file_path) / (1024**3) 
            num_part = f[4:-4] if f.startswith("log_") and f[4:-4].isdigit() else None
            file_list.append((f, size_gb, int(num_part) if num_part else -1))

    file_list.sort(key=lambda x: x[2], reverse=True)

    response = "\n".join([f"📜 {f[0]} - {f[1]:.2f} GB" for f in file_list])
    await event.reply(f"📁 Files in {LOG_PATH}:\n{response}")


# 🗑️ Remove a specific file
@client.on(events.NewMessage(pattern=r"/remove (\S+)"))
async def remove_file(event):
    file_name = event.pattern_match.group(1) 

    if not re.match(r'^[\w,\s-]+\.[A-Za-z]{3}$', file_name):
        await event.reply(f"❌ Invalid file name `{file_name}`.")
        return

    file_path = os.path.join(LOG_PATH, file_name)

    if not os.path.exists(file_path):
        await event.reply(f"❌ File `{file_name}` does not exist.")
    else:
        os.remove(file_path)
        await event.reply(f"✅ File `{file_name}` removed.")


# 📊 Check disk space
@client.on(events.NewMessage(pattern="/space"))
async def check_disk_space(event):
    process = subprocess.run(["df", "-h"], capture_output=True, text=True)
    output = process.stdout

    for line in output.splitlines():
        if "/dev/sda1" in line:  # 📌 # Adjust partition if necessary
            parts = line.split()
            available_space = parts[3] 
            await event.reply(f"📊 Available disk space: `{available_space}`")
            return
    
    await event.reply("⚠️ Could not retrieve disk space information.")


# 🔹 Run the bot
with client:
    client.loop.run_until_complete(main())
    print("🚀 Bot is active and listening for forwarded messages...")
    client.run_until_disconnected()

