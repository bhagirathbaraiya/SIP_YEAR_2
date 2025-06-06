import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token from BotFather
TOKEN = '7515658212:AAGcwB5-MDkAtERW7fLB--7ADoRcEOR2R1U'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    logger.info(f"User {user.first_name} started the bot")
    await update.message.reply_text(f'Hi {user.first_name}! I will log all messages you send.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    logger.info(f"User {update.effective_user.first_name} requested help")
    await update.message.reply_text('Send me any message and I will log it!')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log the received message and echo it back."""
    user = update.effective_user
    message_text = update.message.text
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