from telegram.ext import Application, CommandHandler
from config import TOKEN
from handlers import start, help

# Inicializar o bot
app = Application.builder().token(TOKEN).build()

# Adicionar handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))

# Rodar o bot
print("Bot started")
app.run_polling()
print("Finished")