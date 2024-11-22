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
            "Bem-vindo ao Shop Bot! Escolha uma opção:\n\n" 
            "/catalog - Ver o catálogo de produtos\n"
            "/cart - Ver o carrinho de compras\n\n"
            "Ou clique nos botões abaixo:",
            reply_markup=reply_markup
        )
