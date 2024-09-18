import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = str(os.getenv("TELEGRAM_BOT_TOKEN")) if os.getenv("TELEGRAM_BOT_TOKEN") is not None else ""
if TOKEN == "":
    raise ValueError("A variável de ambiente 'TELEGRAM_BOT_TOKEN' não está definida.")