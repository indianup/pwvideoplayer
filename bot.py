import os
import re
from vars import API_ID, API_HASH, BOT_TOKEN
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

# Get the bot token from environment variables
BOT_TOKEN = os.getenv("7979826252:AAG6PkktURFL-udAd3KipzwiFXp6FEQDbCg")

# Function to extract vid_id from the link
def extract_vid_id(link):
    match = re.search(r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})', link)
    if match:
        return match.group(1)
    return None

# Command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please upload a text file containing lecture or PDF names with their links.")

# Message handler for file upload
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    file_path = f"temp_{update.message.document.file_name}"
    await file.download_to_drive(file_path)
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Parse the file and create a list of (name, vid_id)
    lectures = []
    for line in lines:
        if 'http' in line:
            parts = line.strip().split()
            name = ' '.join(parts[:-1])
            link = parts[-1]
            vid_id = extract_vid_id(link)
            if vid_id:
                lectures.append((name, vid_id))
    
    # Create inline keyboard buttons for each lecture
    keyboard = []
    for name, vid_id in lectures:
        keyboard.append([InlineKeyboardButton(name, callback_data=vid_id)])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select a lecture to play:", reply_markup=reply_markup)
    
    # Clean up the temporary file
    os.remove(file_path)

# Callback query handler for button clicks
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    vid_id = query.data
    player_url = f"https://player.muftukmall.site/?id={vid_id}"
    await query.answer()
    await query.edit_message_text(f"Playing lecture: {player_url}")

# Main function to start the bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.TXT, handle_file))
    application.add_handler(CallbackQueryHandler(button_click))
    
    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
