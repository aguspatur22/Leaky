import os
import subprocess
import time
import json
import datetime
import glob
import asyncio
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler


# Configuration
LOG_DIR = "/path/to/logs"
USER_FILE = "usernames.json"
PROCESSED_LOGS_FILE = "processed_logs.json"
CHAT_ID = "-123456789"
TOKEN = "your_bot_token"


# Load or create username set
def load_usernames():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_usernames(usernames):
    with open(USER_FILE, "w") as f:
        json.dump(list(usernames), f)

# Load or create processed logs set
def load_processed_logs():
    if os.path.exists(PROCESSED_LOGS_FILE):
        with open(PROCESSED_LOGS_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_processed_logs(logs):
    with open(PROCESSED_LOGS_FILE, "w") as f:
        json.dump(list(logs), f)


# Global variables
usernames = load_usernames()
processed_logs = load_processed_logs()
bot = Bot(token=TOKEN)
SEARCH_LOCK = asyncio.Lock()


async def start(update: Update, context: CallbackContext):
    commands = [
        "/start - Show this help message",
        "/register <username> - Register a username in the watchlist",
        "/remove <username> - Remove a username from the watchlist",
        "/list - List all registered usernames",
        "/search <term> - Search for a term in the logs",
    ]
    await update.message.reply_text("✅ Available commands::\n" + "\n".join(commands))


async def register(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("❌ You have to give me a username. Example: /register myusername")
        return
    
    username = context.args[0].strip()
    if username in usernames:
        await update.message.reply_text(f"✅ `{username}` already registered.")
    else:
        usernames.add(username)
        save_usernames(usernames)
        await update.message.reply_text(f"✅ `{username}` added to watchlist.")


async def remove(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("❌ You have to give me a username. Example: /remove myusername")
        return

    username = context.args[0].strip()
    if username in usernames:
        usernames.remove(username)
        save_usernames(usernames)
        await update.message.reply_text(f"✅ `{username}` removed from watchlist.")
    else:
        await update.message.reply_text(f"❌ `{username}` is not in the watchlist.")


async def list_usernames(update: Update, context: CallbackContext):
    if not usernames:
        await update.message.reply_text("ℹ️ No usernames registered.")
    else:
        await update.message.reply_text("👤 Registered usernames:\n" + "\n".join(usernames))


async def search(update: Update, context: CallbackContext):
    if SEARCH_LOCK.locked():
        await update.message.reply_text("❌ The search is already in progress. Please wait a moment.")
        return
    
    if not context.args:
        await update.message.reply_text("❌ You have to give me a search term. Example /search username")
        return
    
    async with SEARCH_LOCK: 
        term = context.args[0]
        chat_id = update.message.chat_id
        user = update.message.from_user.username
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        result_file = f"/tmp/{term}_{now}_{user}.txt"
        
        log_files = glob.glob(os.path.join(LOG_DIR, "*.txt"))
        total_size_gb = sum(os.path.getsize(f) for f in log_files) / (1024 * 1024 * 1024)
        
        await update.message.reply_text(f"🔍 Searching `{term}` in the logs. Wait for a moment, I am checking {total_size_gb:.2f} GBs of data.")

        start_time = time.time()
        try:
            process = await asyncio.create_subprocess_exec(
                'rg', '-i', '--no-filename', '--text', term, *log_files,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            modified_output = []
            for line in stdout.decode().splitlines():
                filename = os.path.basename(line.split(':', 1)[0])
                content = line.split(':', 1)[1]
                modified_output.append(f"{filename}:{content}")
            
            with open(result_file, "w") as f:
                f.write("\n".join(modified_output))
                
            elapsed_time = time.time() - start_time
            elapsed_time_str = f"{elapsed_time:.2f}s" if elapsed_time < 60 else f"{int(elapsed_time // 60)}m {elapsed_time % 60:.2f}s"
            
            if os.path.getsize(result_file) > 0:
                await update.message.reply_text(f"✅ ¡Search completed! So you were leaked hahaha (Time: {elapsed_time_str})\nSending results...")
                await context.bot.send_document(chat_id, open(result_file, "rb"))
            else:
                await update.message.reply_text(f"❌ Perfect! Nothing was found for `{term}`. (Time: {elapsed_time_str})")
        except Exception as e:
            await update.message.reply_text(f"❌ Shit, had an error: {str(e)}")


async def check_new_logs(context: CallbackContext):
    log_files = set(f for f in os.listdir(LOG_DIR) if f.endswith(".txt"))
    new_logs = log_files - processed_logs

    if not new_logs:
        return  

    await bot.send_message(CHAT_ID, f"📂 New log files detected: {', '.join(new_logs)}\nChecking watchlist users...")
    found_leaks = []

    if usernames:
        for username in usernames:
            for log_file in new_logs:
                result = subprocess.run(["grep", "-i", "-a", username, os.path.join(LOG_DIR, log_file)], capture_output=True, text=True)
                if result.stdout:
                    found_leaks.append(f"⚠️ Username `{username}` found in `{log_file}`!")
                    with open(f"/tmp/watchlist_{username}.txt", "w") as f:
                        f.write(result.stdout)
                    
        if found_leaks:
            await bot.send_message(CHAT_ID, "🚨 Users from the watchlist were found in new leaks:")
            for username in usernames:
                file_path = f"/tmp/watchlist_{username}.txt"
                if os.path.exists(file_path):
                    await bot.send_document(CHAT_ID, open(file_path, "rb"))
        else: 
            await bot.send_message(CHAT_ID, "✅ No usernames from the watchlist were found in new logs.")
    
    processed_logs.update(new_logs)
    save_processed_logs(processed_logs)


def main():
    application = Application.builder().token(TOKEN).concurrent_updates(True).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("register", register))
    application.add_handler(CommandHandler("list", list_usernames))
    application.add_handler(CommandHandler("search", search))
    application.add_handler(CommandHandler("remove", remove))

    job_queue = application.job_queue
    job_queue.run_daily(check_new_logs, time=datetime.time(hour=2, minute=0))

    application.run_polling()

if __name__ == "__main__":
    main()
