import logging

from telegram import __version__ as TG_VER
from config import TOKEN



try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    chat_id = update.effective_chat.id

    await context.bot.sendMessage(chat_id=chat_id, text="""
Привіт! 

Напишіть вашу пораду, або зауваження. Це дуже сильно допоможе зробити контент на моїх каналах кращим.

    """)


async def redirect(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    message = update.message.message_id
    chat = await context.bot.get_chat("@qaeliahu")
    await context.bot.forwardMessage(chat_id=chat.id, from_chat_id=update.message.chat_id, message_id=message)
    await context.bot.sendMessage(chat_id=update.effective_chat.id,
                                  text="""Дякую! Якщо вам є, що написати ще, ви можете це зробити будь-коли.""")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, redirect))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()



if __name__ == "__main__":
    main()

