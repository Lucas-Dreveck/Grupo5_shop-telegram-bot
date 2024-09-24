from telegram import Update
from telegram.ext import ContextTypes

async def handle_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text("Você clicou em '📦 Catalogo'. Aqui está o catálogo!")
