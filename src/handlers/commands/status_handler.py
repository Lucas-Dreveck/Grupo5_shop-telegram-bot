from telegram import Update
from telegram.ext import ContextTypes
from utils import fetch_last_order_by_chat_id

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        loading_message = await update.message.reply_text("Buscando status do último pedido...")
        order = fetch_last_order_by_chat_id(update.message.chat_id)
        
        if order is None:
            await update.message.reply_text("Nenhum pedido encontrado.")
            return
        
        await loading_message.edit_text(
            f"Status do pedido:\n\n"
            f"Total: R$ {order['total']}\n"
            f"Status: {order['status_display']}"
        )