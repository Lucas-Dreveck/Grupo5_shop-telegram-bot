from telegram import Update
from telegram.ext import ContextTypes
from .catalog_handler import handle_catalog
from .cart_handler import handle_cart

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.text:
        user_message = update.message.text
        
        if user_message.startswith("/") or (user_message and ord(user_message[0]) >= 1000):
            if user_message == "📦 Catalogo":
                await handle_catalog(update, context)
            elif user_message == "🛒 Carrinho":
                await handle_cart(update, context)
            else:
                await update.message.reply_text("Comando não reconhecido.")
