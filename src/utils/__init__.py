# Cart related imports
from .cart_utils import cart_manager

# Fetching related imports
from .fetching_utils import (
    # Product related
    fetch_product_by_id,
    fetch_products_by_category,
    fetch_catalog,
    
    # Client related
    fetch_client_by_chat_id,
    create_client,
    
    # Order related
    fetch_last_order_by_chat_id,
    create_order,
    
)