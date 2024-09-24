from telegram import Update
from telegram.ext import ContextTypes

async def handle_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text("Você clicou em '🛒 Carrinho'. Aqui está o seu carrinho!")
