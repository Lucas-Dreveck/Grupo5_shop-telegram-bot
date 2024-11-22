# Shop Telegram Bot

A Telegram bot for e-commerce that allows users to browse products, manage their cart, and place orders.

## Prerequisites

- Python 3.12+
- Poetry (Python package manager)
- A Telegram Bot Token ([How to create a Telegram Bot](https://core.telegram.org/bots#how-do-i-create-a-bot))

## Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/Grupo5_shop-telegram-bot.git
cd Grupo5_shop-telegram-bot
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Copy .env.example to .env:
```bash
cp .env.example .env
```

4. Configure your environment variables in .env:
```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
WHATSAPP_NUMBER=your_whatsapp_number
BASE_URL=http://localhost:8000/
```

### Running the Bot
Start the bot with hot reload:
```bash
poetry run watchfiles --filter python 'python .\src\bot.py'
```

Or run without hot reload:
```bash
poetry run python src/bot.py
```

### Available Commands
/start - Start the bot
/catalog - View product catalog
/cart - View shopping cart
/status - Check last order status
/register - Register user information
/help - Get help
/support - Request human support

### Features
📦 Product catalog browsing
🛒 Shopping cart management
💳 Checkout process
📱 WhatsApp support integration
🔄 Order status tracking

### Development
The bot is built using:

python-telegram-bot
Poetry for dependency management
Watchfiles for hot reload during development

### Team
Daniel Hartmann
Eduardo Corrêa
Gabriel Costa
Lucas Dreveck
Mayumi Bogoni
Paola Silva