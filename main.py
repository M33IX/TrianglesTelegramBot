import logging
import TriangleMath
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, CallbackContext, MessageHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    user = update.message.from_user
    await update.message.reply_text(f"Hello {user.first_name}")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    await distribute(text, update, context)

async def distribute(input: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    match(input):
        case "Button 1":
            await sendMessage("lorem ipsum", update, context)
        case "Button 2":
            await sendMessage("sample text", update, context)
        case _:
            await sendMessage("error", update, context)            

async def sendMessage(message: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(message)

if __name__ == '__main__':
    application = ApplicationBuilder().token('7481543119:AAHwWVLmmJUh_JiStOD2Kz5s198kZ-DaylQ').build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~(filters.COMMAND), button_callback))
    
    application.run_polling()