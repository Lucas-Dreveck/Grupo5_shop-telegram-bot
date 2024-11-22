import requests
from config import BACKEND_URL

def fetch_catalog():
    try:
        response = requests.get(f"{BACKEND_URL}categories")
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching catalog: {e}")
        return []

def fetch_products_by_category(category_id: str):
    try:
        response = requests.get(f"{BACKEND_URL}products/category/{category_id}")
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching products: {e}")
        return []
    
def fetch_product_by_id(product_id: str):
    try:
        response = requests.get(f"{BACKEND_URL}products/{product_id}")
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching product: {e}")
        return None
    
def fetch_client_by_chat_id(chat_id: str):
    try:
        response = requests.get(f"{BACKEND_URL}clients/chat/{chat_id}")
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching client: {e}")
        return None

def fetch_last_order_by_chat_id(chat_id: str):
    try:
        response = requests.get(f"{BACKEND_URL}clients/last-order/{chat_id}")
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching order: {e}")
        return None
    
def create_client(client_info: dict):
    try:
        response = requests.post(f"{BACKEND_URL}clients/", json=client_info)
        return response.json()
    except Exception as e:
        print(f"Error creating client: {e}")
        return None
        
def create_order(order_data: dict):
    try:
        response = requests.post(f"{BACKEND_URL}orders/create/", json=order_data)
        return response.json()
    except Exception as e:
        print(f"Error creating order: {e}")
        return None