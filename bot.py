import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# --- Product Identification Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message with the main inline keyboard."""
    keyboard = [
        [InlineKeyboardButton("🧪 Ingredients", callback_data="ingredients")],
        [InlineKeyboardButton("🌍 Country/Region Info", callback_data="region")],
        [InlineKeyboardButton("📦 Product Category", callback_data="category")],
        [InlineKeyboardButton("📋 Package Information", callback_data="package")],
        [InlineKeyboardButton("🔍 Similar Products", callback_data="similar")],
        [InlineKeyboardButton("📝 User Notes", callback_data="notes")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "Welcome to *Forex Academy Extra Trader*! 👋\n\n"
        "Select a product identification option below to get started."
    )
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline button presses for product identification."""
    query = update.callback_query
    await query.answer()

    data = query.data
    response_text = ""

    if data == "ingredients":
        response_text = (
            "*🧪 Ingredients Analysis*\n\n"
            "Please send the product name or a photo of the label. "
            "I will help you identify the active ingredients and potential interactions."
        )
    elif data == "region":
        response_text = (
            "*🌍 Country/Region Information*\n\n"
            "Provide the country or region of origin. I will share relevant regulatory "
            "information and market-specific details."
        )
    elif data == "category":
        response_text = (
            "*📦 Product Category*\n\n"
            "Tell me what the product is (e.g., supplement, cosmetic, food). "
            "I will classify it correctly for your records."
        )
    elif data == "package":
        response_text = (
            "*📋 Package Information*\n\n"
            "Send package details such as size, weight, dimensions, and material. "
            "I will format this for inventory or shipping."
        )
    elif data == "similar":
        response_text = (
            "*🔍 Similar Products*\n\n"
            "Share the product name, and I will suggest similar items based on "
            "category, ingredients, or market trends."
        )
    elif data == "notes":
        response_text = (
            "*📝 User-Created Notes*\n\n"
            "Send me any notes you want to save about a product. "
            "I will keep them organized for future reference."
        )
    else:
        response_text = "Unknown option. Please try again."

    await query.edit_message_text(text=response_text, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle free-text messages (for notes, product names, etc.)."""
    user_input = update.message.text
    user = update.effective_user

    logger.info(f"User {user.id} sent: {user_input}")

    # Echo or process the input — extend this based on your needs
    await update.message.reply_text(
        f"Received: _{user_input}_\n\n"
        "I'll process this information. You can add more details or use /start to go back.",
        parse_mode="Markdown",
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logger.error(f"Update {update} caused error {context.error}")

# --- Application Setup ---

def main() -> None:
    """Start the bot using long polling."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN not set in environment variables.")

    # Create the Application
    application = Application.builder().token(token).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))

    # Callback query handler (inline buttons)
    application.add_handler(CallbackQueryHandler(button_handler))

    # Message handler (non-command text)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # Error handler
    application.add_error_handler(error_handler)

    # Run the bot until the user presses Ctrl-C
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
