from os import environ

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, ConversationHandler, filters

ID_RESULT, ID_CANCEL = range(2)

STT_RESULT, STT_CANCEL = range(2)

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


async def conversation_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Operação Cancelada"
        )
    
    return ConversationHandler.END


async def not_found(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Perdão, não entendi seu comando. Poderia repetir?"
        )

def main():
    app = ApplicationBuilder().token(environ['BOT_TOKEN']).build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = CommandHandler('echo', echo)
    
    # Conversation

    # speach_handler = ConversationHandler(
    #     entry_points=[CommandHandler('gcspeach_transcribe', speach_start)],
    #     states={
    #         ID_RESULT: [
    #             MessageHandler(filters.VOICE, speach_result), 
    #             CommandHandler('cancel', conversation_cancel),
    #             MessageHandler(filters.TEXT, speach_error)
    #             ]
    #     },
    #     fallbacks=[CommandHandler('cancel', conversation_cancel)]
    #     )
    
    # 404
    not_found_handler = MessageHandler(filters.COMMAND, not_found)
    
    # Adicionar handlers
    app.add_handler(start_handler)
    app.add_handler(echo_handler)
    app.add_handler(not_found_handler)
    
    app.run_polling()