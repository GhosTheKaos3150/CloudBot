from os import environ

from google_cloud import vision, stt

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
    
async def identify_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Envie uma imagem a ser analisada!"
        )
    
    return ID_RESULT

async def identify_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    file_bytes = await file.download_as_bytearray()
    
    await vision.get_vision_annotated(file_bytes)
    
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open("generated/vision.png", "rb")
    )
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Aqui está a imagem analisada!"
        )
    
    return ConversationHandler.END


async def identify_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Por favor, envie uma imagem ou digite /cancel para cancelar a operação!"
        )
    
    return ID_RESULT


async def speach_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Envie uma mensagem de voz a ser analisada!"
        )
    
    return STT_RESULT


async def speach_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.voice.get_file()
    file_bytes = await file.download_as_bytearray()
    
    stt.get_stt_transcription(bytes(file_bytes))
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Aqui está a transcrição da mensagem:"
        )
    
    return ConversationHandler.END


async def speach_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Por favor, envie uma mensagem de voz ou digite /cancel para cancelar a operação!"
        )
    
    return STT_RESULT


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
    image_handler = ConversationHandler(
        entry_points=[CommandHandler('gcvision_locate', identify_start)],
        states={
            ID_RESULT: [
                MessageHandler(filters.PHOTO, identify_result), 
                CommandHandler('cancel', conversation_cancel),
                MessageHandler(filters.TEXT, identify_error)
                ]
        },
        fallbacks=[CommandHandler('cancel', conversation_cancel)]
        )

    speach_handler = ConversationHandler(
        entry_points=[CommandHandler('gcspeach_transcribe', speach_start)],
        states={
            ID_RESULT: [
                MessageHandler(filters.VOICE, speach_result), 
                CommandHandler('cancel', conversation_cancel),
                MessageHandler(filters.TEXT, speach_error)
                ]
        },
        fallbacks=[CommandHandler('cancel', conversation_cancel)]
        )
    
    # 404
    not_found_handler = MessageHandler(filters.COMMAND, not_found)
    
    # Adicionar handlers
    app.add_handler(start_handler)
    app.add_handler(echo_handler)
    app.add_handler(image_handler)
    app.add_handler(speach_handler)
    app.add_handler(not_found_handler)
    
    app.run_polling()