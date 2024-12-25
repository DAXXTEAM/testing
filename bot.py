from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from config import API_ID, API_HASH, BOT_TOKEN, users
from github_handler import GitHubHandler
from notification_manager import NotificationManager

# Initialize the bot
bot = Client("github_notification_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
notification_manager = NotificationManager()

@bot.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    await message.reply_text(
        "👋 Welcome to GitHub Notification Bot!\n"
        "Use /login to set up your GitHub token\n"
        "Use /setchat to set notification channel"
    )

@bot.on_message(filters.command("login"))
async def login_command(client: Client, message: Message):
    if len(message.command) != 2:
        await message.reply_text("Please provide your GitHub token:\n/login YOUR_GITHUB_TOKEN")
        return
    
    github_token = message.command[1]
    user_id = str(message.from_user.id)
    
    if user_id not in users:
        users[user_id] = {}
    
    users[user_id]["github_token"] = github_token
    await message.reply_text("✅ GitHub token set successfully!")

@bot.on_message(filters.command("setchat"))
async def setchat_command(client: Client, message: Message):
    if len(message.command) != 2:
        await message.reply_text("Please provide the chat ID:\n/setchat CHAT_ID")
        return
    
    chat_id = message.command[1]
    user_id = str(message.from_user.id)
    
    if user_id not in users:
        await message.reply_text("⚠️ Please set up your GitHub token first using /login")
        return
    
    users[user_id]["chat_id"] = chat_id
    await message.reply_text("✅ Notification chat set successfully!")

async def check_notifications():
    while True:
        for user_id, user_data in users.items():
            if "github_token" not in user_data or "chat_id" not in user_data:
                continue
            
            handler = GitHubHandler(user_data["github_token"])
            try:
                events = await handler.get_notifications()
                for event in events:
                    if event["id"] not in notification_manager.processed_events:
                        notification_text = notification_manager.format_notification(event)
                        await bot.send_message(
                            user_data["chat_id"],
                            notification_text
                        )
                        notification_manager.processed_events.append(event["id"])
            except Exception as e:
                print(f"Error checking notifications for user {user_id}: {e}")
        
        await asyncio.sleep(300)  # Check every 5 minutes

async def main():
    await bot.start()
    print("Bot started...")
    await check_notifications()

if __name__ == "__main__":
    bot.run(main())