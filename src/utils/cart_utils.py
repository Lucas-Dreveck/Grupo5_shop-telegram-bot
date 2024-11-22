from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class CartManager:
    def __init__(self):
        self.cart = {}
        self.loading_states = {}  # Para controlar estados de "Adicionando..."
    
    def add_to_cart(self, user_id, product):
        if user_id not in self.cart:
            self.cart[user_id] = {}
        
        product_id = str(product['id'])
        if product_id in self.cart[user_id]:
            self.cart[user_id][product_id]['quantity'] += 1
        else:
            self.cart[user_id][product_id] = {
                'product': product,
                'quantity': 1
            }
        
        # Remove loading state after adding
        if user_id in self.loading_states:
            self.loading_states[user_id].discard(product_id)
            
        return self.cart[user_id][product_id]['quantity']

    def remove_from_cart(self, user_id, product_id):
        if user_id in self.cart and product_id in self.cart[user_id]:
            if self.cart[user_id][product_id]['quantity'] > 1:
                self.cart[user_id][product_id]['quantity'] -= 1
            else:
                del self.cart[user_id][product_id]
    
    def get_cart(self, user_id):
        return self.cart.get(user_id, {})
    
    def set_loading_state(self, user_id, product_id):
        """Marca um produto como em estado de carregamento"""
        if user_id not in self.loading_states:
            self.loading_states[user_id] = set()
        self.loading_states[user_id].add(product_id)
    
    def is_loading(self, user_id, product_id):
        """Verifica se um produto está em estado de carregamento"""
        return user_id in self.loading_states and product_id in self.loading_states[user_id]
    
    def get_cart_total(self, user_id):
        """Calcula o total de itens no carrinho"""
        if user_id not in self.cart:
            return 0
        return sum(item['quantity'] for item in self.cart[user_id].values())
    
    def create_cart_keyboard(self, user_id, product_id):
        cart_item = self.cart.get(user_id, {}).get(product_id)
        keyboard = []
        
        # Verifica se está em estado de loading
        if self.is_loading(user_id, product_id):
            keyboard.append([
                InlineKeyboardButton("Adicionando...", callback_data="loading")
            ])
        # Se não está no carrinho
        elif not cart_item:
            keyboard.append([
                InlineKeyboardButton("Adicionar ao Carrinho", callback_data=f"add_cart_{product_id}")
            ])
        # Se já está no carrinho
        else:
            quantity = cart_item['quantity']
            keyboard.extend([
                [
                    InlineKeyboardButton("➖", callback_data=f"decrease_cart_{product_id}" if quantity > 1 else "disabled"),
                    InlineKeyboardButton(f"{quantity}", callback_data="quantity"),
                    InlineKeyboardButton("➕", callback_data=f"increase_cart_{product_id}")
                ],
                [InlineKeyboardButton("❌ Remover", callback_data=f"remove_cart_{product_id}")]
            ])
        
        # Adiciona botão de visualizar carrinho se houver itens
        cart_total = self.get_cart_total(user_id)
        if cart_total > 0:
            keyboard.append([
                InlineKeyboardButton(
                    f"🛒 Ver Carrinho ({cart_total} {self._pluralize_items(cart_total)})", 
                    callback_data="view_cart_list"
                )
            ])
        
        return InlineKeyboardMarkup(keyboard)
    
    def _pluralize_items(self, quantity):
        """Retorna a forma plural ou singular de 'item' baseado na quantidade"""
        return "item" if quantity == 1 else "itens"
    
    def clear_cart(self, user_id):
        if user_id in self.cart:
            del self.cart[user_id]
        if user_id in self.loading_states:
            del self.loading_states[user_id]

cart_manager = CartManager()