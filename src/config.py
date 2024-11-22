import os
from dotenv import load_dotenv, find_dotenv
from urllib.parse import quote

load_dotenv(find_dotenv(), override=True)

# Token setup
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("A variável de ambiente 'TELEGRAM_BOT_TOKEN' não está definida.")


# WhatsApp setup
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER")
if not WHATSAPP_NUMBER:
    raise ValueError("A variável de ambiente 'WHATSAPP_NUMBER' não está definida.")

WHATSAPP_NUMBER = ''.join(filter(str.isdigit, WHATSAPP_NUMBER))

DEFAULT_WHATSAPP_MESSAGE = os.getenv("DEFAULT_WHATSAPP_MESSAGE") or "Olá! Gostaria de fazer um pedido."

WHATSAPP_LINK = f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(DEFAULT_WHATSAPP_MESSAGE)}"


# Base URL setup
BASE_URL = os.getenv("BASE_URL")
if not BASE_URL:
    raise ValueError("A variável de ambiente 'BASE_URL' não está definida.")

BACKEND_URL = os.getenv('BACKEND_URL') or f"{BASE_URL}/dashboard/api"
IMAGE_URL = os.getenv('IMAGE_URL') or f"{BASE_URL}"

print("BASE_URL:", BASE_URL)
print("BACKEND_URL:", BACKEND_URL)
print("IMAGE_URL:", IMAGE_URL)