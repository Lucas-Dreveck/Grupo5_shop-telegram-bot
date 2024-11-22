from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler, MessageHandler, CommandHandler, filters
from utils import cart_manager, fetch_client_by_chat_id, create_order, create_client
from config import IMAGE_URL

# Define conversation states
(
    AWAITING_NAME,
    AWAITING_PHONE,
    AWAITING_CITY,
    AWAITING_ADDRESS,
    AWAITING_CONFIRMATION
) = range(5)

async def start_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Inicia o processo de checkout e redireciona para o registro"""
    query = update.callback_query
    user_id = query.from_user.id
    
    # Get cart contents
    cart = cart_manager.get_cart(user_id)
    
    if not cart:
        await query.answer("Seu carrinho está vazio!")
        return
    
    # Calculate total and prepare items for order
    total = 0
    order_items = []
    
    for product_id, item_data in cart.items():
        product = item_data['product']
        quantity = item_data['quantity']
        price = float(product['price'])
        item_total = price * quantity
        total += item_total
        
        order_items.append({
            "product": int(product_id),
            "quantity": quantity,
            "price": price
        })
    
    # Prepare order data
    order_data = {
        "client_chat_id": user_id,
        "total": total,
        "items": order_items
    }
    
    # Store order data in context for later use
    context.user_data['waiting_payment'] = order_data
    
    client = fetch_client_by_chat_id(user_id)

    if client:
        context.user_data['client_info'] = client
        
        # Proceed to checkout
        await query.answer()
        return await finish_order(update, context)
    
    # Start client registration process
    await query.answer()
    await query.edit_message_text(
        "🛍️ Seu pedido está sendo processado!\n\n"
        "Para finalizar, precisamos de algumas informações.\n\n"
        "Use o comando /register para começar o cadastro."
    )

async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inicia o processo de registro"""
    loading_message = await update.message.reply_text("Procurando cadastro...")
    client = fetch_client_by_chat_id(update.effective_user.id)
    
    if client:
        await loading_message.edit_text(
            "Você já está registrado!"
        )
        return ConversationHandler.END
    
    # Verifica se há um pedido em andamento
    has_pending_order = 'waiting_payment' in context.user_data
    
    message = (
        "👤 Vamos começar seu cadastro!\n\n"
    )
    
    if has_pending_order:
        message += (
            "🛍️ Notei que você tem um pedido em andamento.\n"
            "Após o cadastro, você será redirecionado para finalizar sua compra.\n\n"
        )
    
    message += "Por favor, digite seu nome completo:"
    
    await loading_message.edit_text(message)
    return AWAITING_NAME

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the name input and request phone number"""
    name = update.message.text
    context.user_data['client_info'] = {"name": f"{name}"}
    
    await update.message.reply_text(
        "📱 Ótimo! Agora, por favor, digite seu número de telefone:\n"
        "(Exemplo: +55 11 99999-9999)"
    )
    return AWAITING_PHONE

async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the phone input and request city"""
    phone = update.message.text
    context.user_data['client_info']["phone_number"] = f"{phone}"
    
    await update.message.reply_text(
        "🏘️ Perfeito! Agora digite sua cidade:"
    )
    return AWAITING_CITY

async def handle_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the city input and request address"""
    city = update.message.text
    context.user_data['client_info']["city"] = f"{city}"
    
    await update.message.reply_text(
        "📍 Por último, digite seu endereço completo:\n"
        "(Rua, número, complemento, bairro e CEP)"
    )
    return AWAITING_ADDRESS

async def handle_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the address input and complete the registration"""
    address = update.message.text
    
    context.user_data['client_info']["address"] = f"{address}"
    
    await update.message.reply_text(
        "🔒 Confirme as informações abaixo:\n\n"
        f"Nome: {context.user_data['client_info']['name']}\n"
        f"Telefone: {context.user_data['client_info']['phone_number']}\n"
        f"Cidade: {context.user_data['client_info']['city']}\n"
        f"Endereço: {context.user_data['client_info']['address']}\n\n"
        "Se estiver tudo correto, use o comando /confirm para finalizar o cadastro.\n"
        "Caso contrário, use o comando /cancel para cancelar o cadastro."
    )
    
    return AWAITING_CONFIRMATION

async def finish_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Finish the registration process"""
    user_id = update.effective_user.id
    
    # Complete client info
    client_info = context.user_data['client_info']
    client_info.update({
        "chat_id": f"{str(user_id)}",
        "is_active": "true"
    })
    
    # Create client
    create_client(client_info)
    
    # Check if there's a pending order
    if 'waiting_payment' in context.user_data:
        await update.message.reply_text(
            "✅ Cadastro realizado com sucesso!\n"
            "Agora vamos finalizar seu pedido."
        )
        return await finish_order(update, context)
    else:
        await update.message.reply_text(
            "✅ Cadastro realizado com sucesso!\n\n"
            "Você já pode fazer pedidos usando o comando /start"
        )
        context.user_data.clear()
        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the registration process"""
    has_pending_order = 'waiting_payment' in context.user_data
    
    if has_pending_order:
        message = (
            "Processo de cadastro cancelado. Seu carrinho foi mantido.\n"
            "Para tentar novamente, use o comando /cart"
        )
    else:
        message = (
            "Processo de cadastro cancelado.\n"
            "Para tentar novamente, use o comando /register"
        )
    
    await update.message.reply_text(message)
    
    # Clear only client_info, maintaining cart if it exists
    if 'client_info' in context.user_data:
        del context.user_data['client_info']
    
    return ConversationHandler.END

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
import requests
from io import BytesIO

async def finish_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        # Create order
        order_data = context.user_data['waiting_payment']
        pix_qr_code = create_order(order_data)
        pix_qr_code_url = pix_qr_code["qr_code_url"]
        pix_key = pix_qr_code['pix_key']
        
        if update.message:
            send_message = update.message.reply_text
            send_photo = update.message.reply_photo
        elif update.callback_query:
            await update.callback_query.answer()
            send_message = update.callback_query.message.reply_text
            send_photo = update.callback_query.message.reply_photo
        else:
            raise ValueError("Neither message nor callback_query found in update")
        
        await send_message(
            "✅ Seu pedido foi realizado com sucesso!\n\n"
            f"📦 Total: R$ {order_data['total']:.2f}\n\n"
            "Agora, efetue o pagamento usando a chave PIX abaixo:"
        )
        
        try:
            response = requests.get(IMAGE_URL + pix_qr_code_url)
            response.raise_for_status()
            
            img_bytes = BytesIO(response.content)
            
            await send_photo(
                photo=img_bytes,
                caption=f"Chave PIX: {pix_key}"
            )
        except requests.RequestException as e:
            print(f"Erro ao baixar a imagem: {e}")
            await send_message(
                "❌ Não foi possível carregar o QR code.\n"
                f"Use a chave PIX para fazer o pagamento: {pix_key}"
            )
        
        context.user_data.clear()
        
        user_id = update.effective_user.id
        cart_manager.clear_cart(user_id)
                
    except Exception as e:
        print(f"Error during checkout: {e}")
        error_message = (
            "❌ Desculpe, ocorreu um erro ao processar seu pedido.\n"
            "Por favor, tente novamente mais tarde ou entre em contato com nosso suporte."
        )
        
        try:
            if update.message:
                await update.message.reply_text(error_message)
            elif update.callback_query:
                await update.callback_query.message.reply_text(error_message)
        except Exception as send_error:
            print(f"Error sending error message: {send_error}")
    
    return ConversationHandler.END

# Separate handlers for checkout and registration
checkout_handler = CallbackQueryHandler(start_checkout, pattern=r"^checkout$")

registration_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("register", start_registration)],
    states={
        AWAITING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)],
        AWAITING_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_phone)],
        AWAITING_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_city)],
        AWAITING_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_address)],
        AWAITING_CONFIRMATION: [CommandHandler("confirm", finish_registration)]
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)