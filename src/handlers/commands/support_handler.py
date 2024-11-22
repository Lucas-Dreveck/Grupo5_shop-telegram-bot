from telegram import Update
from telegram.ext import ContextTypes
from config import WHATSAPP_LINK

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        '<b>Suporte Shop Bot</b> 🛠\n\n'
        'Para suporte, entre em contato através do WhatsApp!\n\n'
        f'<a href="{WHATSAPP_LINK}">Clique aqui para abrir o WhatsApp</a>'
    )
    
    await update.message.reply_text(
        message,
        parse_mode='HTML',
        disable_web_page_preview=True
    )