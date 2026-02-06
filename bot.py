import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from pymongo import MongoClient
import os

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB setup
client = MongoClient(os.getenv("MONGO_URI"))  # Use an environment variable for Mongo URI
db = client['telegram_bot_db']
button_collection = db['buttons']
user_collection = db['users']

# Global variables for sudo users
SUDO_USERS = [os.getenv("SUDO_USER_ID")]  # Use an environment variable for SUDO user ID

def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    # Register the user if not already in the DB
    if user_collection.find_one({"user_id": user_id}) is None:
        user_collection.insert_one({"user_id": user_id, "buttons_used": 0})

    # Send the permanent start message
    welcome_message = "Welcome to ADrama Lovers! Select the drama category and press the button for the drama you need."
    update.message.reply_text(welcome_message, reply_markup=categories_keyboard())

def categories_keyboard():
    # Retrieve categories from MongoDB and generate keyboard
    categories = button_collection.distinct("category")
    buttons = [[InlineKeyboardButton(cat, callback_data=f"category_{cat}")] for cat in categories]
    return InlineKeyboardMarkup(buttons)

def category_buttons(update: Update, context: CallbackContext):
    query = update.callback_query
    category = query.data.split("_")[1]
    buttons = button_collection.find({"category": category})
    
    button_list = [
        [InlineKeyboardButton(button['name'], url=button['link'])] for button in buttons
    ]
    
    query.edit_message_text(text=f"Choose a link from {category} category:", reply_markup=InlineKeyboardMarkup(button_list))

def add_button(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in SUDO_USERS:
        update.message.reply_text("You are not authorized to perform this action.")
        return
    
    try:
        category, name, link = context.args
        button_collection.insert_one({"category": category, "name": name, "link": link})
        update.message.reply_text(f"Button '{name}' added under category '{category}' with link '{link}'")
    except ValueError:
        update.message.reply_text("Usage: /add_button <category> <name> <link>")

def edit_button(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in SUDO_USERS:
        update.message.reply_text("You are not authorized to perform this action.")
        return
    
    try:
        button_id, name, link = context.args
        button_collection.update_one({"_id": button_id}, {"$set": {"name": name, "link": link}})
        update.message.reply_text(f"Button '{name}' updated with new link '{link}'")
    except ValueError:
        update.message.reply_text("Usage: /edit_button <button_id> <name> <link>")

def delete_button(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in SUDO_USERS:
        update.message.reply_text("You are not authorized to perform this action.")
        return
    
    try:
        button_id = context.args[0]
        button_collection.delete_one({"_id": button_id})
        update.message.reply_text(f"Button with ID '{button_id}' deleted.")
    except ValueError:
        update.message.reply_text("Usage: /delete_button <button_id>")

def bot_stats(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in SUDO_USERS:
        update.message.reply_text("You are not authorized to view stats.")
        return
    
    total_users = user_collection.count_documents({})
    total_buttons = button_collection.count_documents({})
    update.message.reply_text(f"Total Users: {total_users}\nTotal Buttons: {total_buttons}")

def handle_button(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data.startswith('category_'):
        category_buttons(update, context)
    query.answer()

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")  # Use an environment variable for bot token
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('add_button', add_button, pass_args=True))
    dispatcher.add_handler(CommandHandler('edit_button', edit_button, pass_args=True))
    dispatcher.add_handler(CommandHandler('delete_button', delete_button, pass_args=True))
    dispatcher.add_handler(CommandHandler('bot_stats', bot_stats))

    dispatcher.add_handler(CallbackQueryHandler(handle_button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
