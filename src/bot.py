from telegram.ext import Application
from config import TOKEN
from handlers import set_handlers, add_handlers

def main():
    # Inicializar o bot
    app = Application.builder().token(TOKEN).post_init(set_handlers).build()

    # Adicionar handlers
    add_handlers(app)

    # Rodar o bot
    print("Bot started")
    app.run_polling()
    print("Finished")

if __name__ == "__main__":
    main()