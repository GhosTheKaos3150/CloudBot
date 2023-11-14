from os import environ

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Olá! Mande um audio que eu envio a sua tradução!"
        )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.replace('/echo', '').lstrip()
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"BOT: {msg}"
        )

async def not_found(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Perdão, não entendi seu comando. Poderia repetir?"
        )

def main():
    app = ApplicationBuilder().token(environ['BOT_TOKEN']).build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = CommandHandler('echo', echo)
    
    # 404
    not_found_handler = MessageHandler(filters.COMMAND, not_found)
    
    # Adicionar handlers
    app.add_handler(start_handler)
    app.add_handler(echo_handler)
    app.add_handler(not_found_handler)
    
    app.run_polling()