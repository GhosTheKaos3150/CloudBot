from os import environ
from aws_module import aws_s3

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, ConversationHandler, filters

S3_SEND_RESULT, S3_SEND_CANCEL = range(2)
S3_GET_RESULT, S3_GET_CANCEL = range(2)


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


async def send_video_to_S3_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Envie um vídeo a ser analisado!"
    )
    
    return S3_SEND_RESULT


async def send_video_to_S3_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    file = await update.message.video.get_file()
    file_name = update.message.video.file_name
    file_bytes = await file.download_as_bytearray()
    
    aws_s3.send_video_to_s3(file_bytes, file_name)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"A análise pode demorar até 5 minutos para ser concluída."
        )
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"O nome de seu objeto é {file_name.split('.')[0]}!\nAnote este nome para recuperar dados mais tarde."
        )
    
    return ConversationHandler.END


async def get_files_from_S3_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Envie um nome a ser recuperado!"
    )
    
    return S3_GET_RESULT


async def get_files_from_S3_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    file_name=update.message.text
    labels, subtitles = aws_s3.get_video_data_from_s3(file_name)
    
    if labels == 500:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            
            text=f"Não foi possível recuperar este arquivo.\nVocê escreveu seu nome corretamente?"
            )
        
        return ConversationHandler.END
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=labels
        )
    
    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=subtitles,
        filename=file_name+".srt"
        )
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Retorno get_from_S3"
        )
    
    return ConversationHandler.END


async def get_files_from_S3_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Por favor, envie um nome de arquivo válido, sem extensão."
        )
    
    return S3_GET_RESULT


async def send_video_to_S3_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Por favor, envie um vídeo ou digite /cancel para cancelar a operação!"
        )
    
    return S3_SEND_RESULT


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

    send_S3_handler = ConversationHandler(
        entry_points=[CommandHandler('aws_s3_send', send_video_to_S3_start)],
        states={
            S3_SEND_RESULT: [
                MessageHandler(filters.VIDEO, send_video_to_S3_result), 
                CommandHandler('cancel', conversation_cancel),
                MessageHandler(filters.TEXT, send_video_to_S3_error)
                ]
        },
        fallbacks=[CommandHandler('cancel', conversation_cancel)]
        )

    get_S3_handler = ConversationHandler(
        entry_points=[CommandHandler('aws_s3_retrieve', get_files_from_S3_start)],
        states={
            S3_SEND_RESULT: [
                MessageHandler(filters.TEXT, get_files_from_S3_end), 
                CommandHandler('cancel', conversation_cancel),
                MessageHandler(filters.ALL, get_files_from_S3_error)
                ]
        },
        fallbacks=[CommandHandler('cancel', conversation_cancel)]
        )
    
    # 404
    not_found_handler = MessageHandler(filters.COMMAND, not_found)
    
    # Adicionar handlers
    app.add_handler(start_handler)
    app.add_handler(echo_handler)
    app.add_handler(send_S3_handler)
    app.add_handler(get_S3_handler)
    app.add_handler(not_found_handler)
    
    app.run_polling()