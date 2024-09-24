from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    btnCatalog = KeyboardButton("📦 Catalogo")
    btnCart = KeyboardButton("🛒 Carrinho")

    keyboard = [
        [btnCatalog],
        [btnCart]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    if update.message:
        await update.message.reply_text(
            "Bem-vindo ao Shop Bot! Escolha uma opção:", 
            reply_markup=reply_markup
        )
