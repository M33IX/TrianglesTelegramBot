import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

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
    keyboard = list()
    for i in range(count):
        keyboard.append([InlineKeyboardButton(f'Button {i+1}', callback_data=f'button_{i+1}')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Ваши кнопки:', reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f'Вы нажали кнопку: {query.data}')

if __name__ == '__main__':
    application = ApplicationBuilder().token('7481543119:AAHwWVLmmJUh_JiStOD2Kz5s198kZ-DaylQ').build()
    
    start_handler = CommandHandler('start', start)
    buttons_handler = CommandHandler('buttons', buttons)
    application.add_handler(start_handler)
    application.add_handler(buttons_handler)
    application.add_handler(CallbackQueryHandler(button_callback))
    
    application.run_polling()