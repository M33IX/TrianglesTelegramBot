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
    await update.message.reply_text(f"Здарова пидр {user.first_name}")

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        count = int(context.args[0])
    except (IndexError, ValueError):
        await update.message.reply_text('Пожалуйста, укажите количество кнопок после команды /buttons.')
        return

    keyboard = []
    for i in range(count):
        keyboard.append([KeyboardButton(f'Button {i+1}')])

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=False, one_time_keyboard=False)
    await update.message.reply_text('Ваши кнопки:', reply_markup=reply_markup)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    await update.message.reply_text(f'Вы нажали кнопку: {text}')

if __name__ == '__main__':
    application = ApplicationBuilder().token('7481543119:AAHwWVLmmJUh_JiStOD2Kz5s198kZ-DaylQ').build()
    
    start_handler = CommandHandler('start', start)
    buttons_handler = CommandHandler('buttons', buttons)
    application.add_handler(start_handler)
    application.add_handler(buttons_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~(filters.COMMAND), button_callback))
    
    application.run_polling()