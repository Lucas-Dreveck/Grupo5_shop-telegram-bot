from telegram import Update
from telegram.ext import ContextTypes

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(
            "Este é um bot de e-commerce.\n\n"
            "Você pode usar os seguintes comandos:\n\n"
            "/start - Iniciar o bot\n"
            "/catalog - Ver o catálogo de produtos\n"
            "/cart - Ver o carrinho de compras\n"
            "/status - Verificar o status do seu último pedido\n"
            "/help - Obter ajuda\n"
            "/support - Pedir atendimento humano\n"
            "/register - Se registrar após finalizar um pedido\n\n"
            "Para começar, utilize do /catalog ou clique no botão abaixo:"
        )
