from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from utils import fetch_catalog

async def handle_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        loading_message = await update.message.reply_text("Buscando categorias...")
        
        categories = fetch_catalog()
        
        if categories is None:
            await loading_message.edit_text("Erro ao buscar categorias.")
            return
        elif categories == []:
            await loading_message.edit_text("Nenhuma categoria encontrada.")
            return
        
        buttons = [
            [InlineKeyboardButton(text=f"{category['name']}", switch_inline_query_current_chat=f"{category['name']}")]
            for category in categories
        ]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        
        # Editamos a mensagem de loading ao invés de enviar uma nova
        await loading_message.edit_text(
            "Escolha uma categoria para ver os produtos:",
            reply_markup=reply_markup
        )