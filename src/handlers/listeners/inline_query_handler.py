from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils import cart_manager, fetch_catalog, fetch_products_by_category


async def handle_inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query
    if not query or not query.query:
        return

    try:
        categories = fetch_catalog()
        
        if categories is None:
            await query.answer([])
            return
        elif categories == []:
            await query.answer([])
            return
        
        matching_category = next((cat for cat in categories if cat['name'].lower() == query.query.lower()), None)
        
        if not matching_category:
            await query.answer([])
            return

        products = fetch_products_by_category(str(matching_category['id']))
        
        results = []
        for product in products:
            keyboard = cart_manager.create_cart_keyboard(query.from_user.id, str(product['id']))
            
            image = product.get('image_url', '')
            
            message_text = (
                f'<a href="{image}" width="300" height="300"> </a>'
                f'<b>Nome:</b> {product["name"]}\n'
                f'<b>Descrição:</b> {product.get("description", "")}\n'
                f'<b>Preço:</b> R${product["price"]}'
            )
            

            results.append(
                    InlineQueryResultArticle(
                    id=product['id'],
                    title=product['name'],
                    description=f"R$ {product['price']}".replace('.', ','),
                    thumbnail_url=image,
                    input_message_content=InputTextMessageContent(
                        message_text=message_text,
                        parse_mode=ParseMode.HTML
                    ),
                    reply_markup=keyboard
                )
            )
        
        await query.answer(results, cache_time=0)
    except Exception as e:
        print(f"Error in inline query: {e}")
        await query.answer([])