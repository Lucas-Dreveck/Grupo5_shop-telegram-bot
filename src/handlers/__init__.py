from telegram import BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from .commands.start_handler import start
from .commands.help_handler import help
from .listeners.message_handler import handle_message

async def set_handlers(app: Application) -> None:
    await app.bot.set_my_commands([
        BotCommand("start", "Iniciar o bot"),
        BotCommand("help", "Obter ajuda")
    ])

def add_handlers(app: Application) -> None:
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

