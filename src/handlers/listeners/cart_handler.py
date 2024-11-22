from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils import cart_manager, fetch_product_by_id


async def handle_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Função para exibir o carrinho do usuário
    """
    user_id = update.effective_user.id
    cart = cart_manager.get_cart(user_id)
    
    if not cart:
        if update.callback_query:
            await update.callback_query.message.reply_text("Seu carrinho está vazio.")
        else:
            await update.message.reply_text("Seu carrinho está vazio.")
        return
    
    cart_message = await get_cart_message(user_id)
    
    keyboard = get_cart_keyboard()
    
    # Handle both command and callback query
    if update.callback_query:
        await update.callback_query.message.reply_text(
            cart_message, 
            parse_mode='Markdown', 
            reply_markup=keyboard
        )
    else:
        await update.message.reply_text(
            cart_message, 
            parse_mode='Markdown', 
            reply_markup=keyboard
        )

async def handle_cart_actions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    chat_id = query.message.chat.id if query.message and query.message.chat else user_id
    
    try:
        parts = query.data.split('_')
        
        if len(parts) < 3:
            print(f"Invalid callback data format: {query.data}")
            await query.answer("Invalid action")
            return
            
        action = parts[0]  # add, remove, increase, decrease
        product_id = parts[2]
        
        await query.answer()
        
        cart = cart_manager.get_cart(user_id)
        
        if action == "clear":
            cart_manager.clear_cart(user_id)
            await query.edit_message_text("Carrinho limpo.")
            return
        
        if action == "view":
            await query.answer()
            cart_message = await get_cart_message(user_id)
            keyboard = get_cart_keyboard()
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=cart_message,
                parse_mode='Markdown',
                reply_markup=keyboard
            )
            return
        
        cart_item = cart.get(product_id)
        
        if cart_item is None and action == 'add':
            cart_manager.set_loading_state(user_id, product_id)
            await query.edit_message_reply_markup(
                reply_markup=cart_manager.create_cart_keyboard(user_id, product_id)
            )  
            product = fetch_product_by_id(product_id)
            if not product:
                await query.message.reply_text("Produto não encontrado.")
                return
            quantity = cart_manager.add_to_cart(user_id, product)
            cart_item = cart_manager.get_cart(user_id).get(product_id)
        else:
            if cart_item:
                product = cart_item['product']
                if action == 'remove':
                    cart_manager.remove_from_cart(user_id, product_id)
                elif action == 'increase':
                    quantity = cart_manager.add_to_cart(user_id, product)
                elif action == 'decrease':
                    cart_manager.remove_from_cart(user_id, product_id)
                
                cart_item = cart_manager.get_cart(user_id).get(product_id)
            else:
                await query.message.reply_text("Produto não encontrado no carrinho.")
                return
        
        if not cart_item:
            try:
                # Show product removed message
                await query.edit_message_text(
                    text="Produto removido do carrinho.",
                    parse_mode=ParseMode.HTML
                )
            except Exception as e:
                print(f"Error updating message after removal: {e}")
            return
        
        quantity = cart_item['quantity']
        price = float(product['price'])
        total = price * quantity
        
        new_keyboard = cart_manager.create_cart_keyboard(user_id, product_id)
        
        message_text = (
            f'<a href="{product.get("image_url", "")}" width="300" height="300"> </a>\n'
            f'<b>Nome:</b> {product["name"]}\n'
            f'<b>Descrição:</b> {product.get("description", "")}\n'
            f'<b>Preço unitário:</b> R${price:.2f}\n'
            f'<b>Quantidade:</b> {quantity}\n'
            f'<b>Subtotal:</b> R${total:.2f}'
        )
        
        try:
            await query.edit_message_text(
                text=message_text,
                parse_mode=ParseMode.HTML,
                reply_markup=new_keyboard
            )
        except Exception as e:
            print(f"Error updating message: {e}")
            await query.message.reply_text(
                text=message_text,
                parse_mode=ParseMode.HTML,
                reply_markup=new_keyboard
            )
            
    except Exception as e:
        print(f"Error processing callback: {e}")
        await query.answer("Erro ao processar ação")
        
def get_cart_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Finalizar Compra", callback_data="checkout")],
        [InlineKeyboardButton("Limpar Carrinho", callback_data="clear_cart_list")]
    ])

async def get_cart_message(user_id):
    cart = cart_manager.get_cart(user_id)
    if not cart:
        return "Seu carrinho está vazio."
        
    cart_message = "🛒 Seu Carrinho:\n\n"
    total = 0
    
    for product_id, item_data in cart.items():
        product = item_data['product']
        quantity = item_data['quantity']
        item_total = float(product['price']) * quantity
        total += item_total
        
        cart_message += (
            f"*{product['name']}*\n"
            f"Quantidade: {quantity}\n"
            f"Preço unitário: R$ {product['price']}\n"
            f"Subtotal: R$ {item_total:.2f}\n\n"
        )
    
    cart_message += f"*Total do Carrinho: R$ {total:.2f}*"
    return cart_message