from telegram import BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, InlineQueryHandler

from .commands.start_handler import start
from .listeners.catalog_handler import handle_catalog
from .listeners.cart_handler import handle_cart
from .commands.status_handler import status
from .commands.help_handler import help
from .commands.support_handler import support

from .listeners.message_handler import handle_message

from .listeners.cart_handler import handle_cart_actions
from .listeners.checkout_handler import checkout_handler, registration_conv_handler

from .listeners.inline_query_handler import handle_inline_query

async def set_handlers(app: Application) -> None:
    await app.bot.set_my_commands([
        BotCommand("start", "Iniciar o bot"),
        BotCommand("status", "Verificar o status do seu último pedido"),
        BotCommand("register", "Se cadastrar"),
        BotCommand("help", "Obter ajuda"),
        BotCommand("support", "Pedir atendimento humano"),
    ])

def add_handlers(app: Application) -> None:
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("catalog", handle_catalog))
    app.add_handler(CommandHandler("cart", handle_cart))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("support", support))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(registration_conv_handler)
    
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_handler(CallbackQueryHandler(handle_cart_actions, pattern=r"^(add|remove|increase|decrease|clear|view)_cart_.*$"))
    app.add_handler(checkout_handler)
    
    app.add_handler(InlineQueryHandler(handle_inline_query))
    
    