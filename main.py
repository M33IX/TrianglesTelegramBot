import logging
from mailbox import Message
from types import NoneType

from numpy import tri
from TriangleMath import Triangle
import re
from telegram import (
    Update, 
    KeyboardButton, 
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
    )
from telegram.ext import( 
    ApplicationBuilder, 
    ContextTypes, 
    CommandHandler, 
    filters, 
    MessageHandler,
    ConversationHandler
    )

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

first_start_keyboard = [["Создать новый треугольник"], ["Закончить"]]
fs_markup = ReplyKeyboardMarkup(
    first_start_keyboard, 
    one_time_keyboard=True, 
    input_field_placeholder="Выберите действие",
    resize_keyboard=True
    )
menu_keyboard = [
    ["Вычислить все параметры треугольника"],
    ["Закончить"],
]
markup = ReplyKeyboardMarkup(
    menu_keyboard,
    one_time_keyboard=False,
    input_field_placeholder="Выберите действие",
    resize_keyboard=True
)

logging.getLogger("httpx").setLevel(logging.WARNING)

CREATION, CHOOSING, STARTMENU = range(3)

triangle = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начинает беседу с юзером"""
    user = update.message.from_user
    await update.message.reply_text(f"Привет, {user.first_name}!", reply_markup=fs_markup)
    return STARTMENU

async def create_triangle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    userInput = update.message.text

    try:
        a, b, c = map(float, userInput.split())
    except:
        await update.message.reply_text(
            "Неправильный ввод, попробуйте еще раз", 
            reply_markup=fs_markup)
        return STARTMENU
    global triangle
    try:
        triangle = Triangle(a,b,c)
    except:
        await update.message.reply_text(
            "Ошибка! Треугольник с данными сторонами не может существовать\n"
                "Попробуйте еще раз", 
                reply_markup=fs_markup)
        return STARTMENU
    await update.message.reply_text("Треугольник создан успешно", reply_markup=markup)
    return CHOOSING

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Завершение работы...", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def creation_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Введите стороны\nПример: 3.0 4.0 5.0 ", reply_markup=ReplyKeyboardRemove())
    return CREATION

async def calculate_triangle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if triangle is None:
        await update.message.reply_text("Что-то пошло не так, повторите попытку позже", reply_markup=None)
        return ConversationHandler.END
    await update.message.reply_text(f"{triangle.toString()}", reply_markup=fs_markup)
    return STARTMENU

def main() -> None:
    application = ApplicationBuilder().token("7481543119:AAHwWVLmmJUh_JiStOD2Kz5s198kZ-DaylQ").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CREATION: [
                MessageHandler(
                    filters.Regex(r"^\d+(\.\d+)?\s\d+(\.\d+)?\s\d+(\.\d+)?$"), create_triangle
                )
            ],
            CHOOSING: [
                MessageHandler(
                    filters.Regex("^Вычислить все параметры треугольника$"), calculate_triangle
                )
            ],
            STARTMENU: [
                MessageHandler(
                    filters.Regex("^Создать новый треугольник$"), creation_menu
                )
            ]

        },
        fallbacks=[MessageHandler(filters.Regex("^Закончить$"), cancel)]
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()