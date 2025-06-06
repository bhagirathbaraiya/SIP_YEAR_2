import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from datetime import datetime
import traceback

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Firebase configuration
FIREBASE_URL = "https://crud-31724-default-rtdb.firebaseio.com"
FIREBASE_API_KEY = "AIzaSyC6TcmVZQvpSvzIGvuTVXLY-KYJb_De8sw"

# Replace 'YOUR_BOT_TOKEN' with your actual bot token from BotFather
TOKEN = '7515658212:AAGcwB5-MDkAtERW7fLB--7ADoRcEOR2R1U'

async def check_user_exists(user_id):
    """Check if a user exists in Firebase."""
    try:
        url = f"{FIREBASE_URL}/users/{user_id}.json"
        response = requests.get(url)
        return response.status_code == 200 and response.json() is not None
    except Exception as e:
        logger.error(f"Error checking user existence: {str(e)}")
        return False

async def save_user_details(user):
    """Save user details to Firebase."""
    try:
        user_data = {
            'user_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'first_seen': datetime.now().isoformat()
        }
        
        url = f"{FIREBASE_URL}/users/{user.id}.json"
        response = requests.put(url, json=user_data)
        
        if response.status_code == 200:
            logger.info(f"User details saved successfully for user {user.first_name}")
        else:
            logger.error(f"Failed to save user details. Status code: {response.status_code}")
            
    except Exception as e:
        logger.error(f"Error saving user details: {str(e)}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    logger.info(f"User {user.first_name} started the bot")
    
    # Check if user exists and save if not
    if not await check_user_exists(user.id):
        await save_user_details(user)
    
    await update.message.reply_text(f'Hi {user.first_name}! I will log all messages you send.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    logger.info(f"User {update.effective_user.first_name} requested help")
    await update.message.reply_text('Send me any message and I will log it!')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log the received message and echo it back."""
    user = update.effective_user
    message_text = update.message.text
    
    # Check if user exists and save if not
    if not await check_user_exists(user.id):
        await save_user_details(user)
    
    # Create message data
    message_data = {
        'user_id': user.id,
        'message_text': message_text,
        'timestamp': datetime.now().isoformat(),
        'chat_id': update.effective_chat.id,
        'message_id': update.message.message_id
    }
    
    # Save message to Firebase Realtime Database using REST API
    try:
        logger.info(f"Attempting to save message to Firebase: {message_data}")
        
        # Construct the URL for the REST API
        url = f"{FIREBASE_URL}/telegram_messages.json"
        
        # Make the POST request
        response = requests.post(url, json=message_data)
        
        # Check if the request was successful
        if response.status_code == 200:
            logger.info(f"Message saved successfully. Response: {response.json()}")
        else:
            logger.error(f"Failed to save message. Status code: {response.status_code}, Response: {response.text}")
            
    except Exception as e:
        logger.error(f"Error saving message to Firebase: {str(e)}")
        logger.error(traceback.format_exc())
    
    logger.info(f"Received message from {user.first_name}: {message_text}")
    await update.message.reply_text(f'You said: {message_text}')

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main() 