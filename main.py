import logging
from TriangleMath import Triangle
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

triangle = None

def defaultkeyboard() -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(f'Создать новый треугольник')]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    return reply_markup
def setupkeyboard() -> ReplyKeyboardMarkup:
    keyboard = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    await update.message.reply_text(f"Hello {user.first_name}", reply_markup=defaultkeyboard())

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    await distribute(text, update, context)

async def distribute(input: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    match(input):
        case "Создать новый треугольник":
            await createTriangle(update, context)
            await sendMessage("lorem ipsum", update, context)
        case "Вывести все рассчитанные параметры":
            await sendMessage("sample text", update, context)
        case "Рассчитать углы":
            await sendMessage("sample text", update, context)
        case "Вычислить перимтер":
            await sendMessage("sample text", update, context)
        case "Опредилить тип треугольника":
            await sendMessage("sample text", update, context)
        case "Вычислить площадь":
            await sendMessage("sample text", update, context)
        case "Вычислить высоты":
            await sendMessage("sample text", update, context)
        case "Вычислить медианы":
            await sendMessage("sample text", update, context)
        case "Вычислить биссектрисы":
            await sendMessage("sample text", update, context)
        case _:
            await sendMessage("Неправильный ввод. Попробуйте еще раз", update, context)

async def createTriangle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Введите стороны треугольника через проебел\nПример: A B C", reply_markup=None)
    userInput = update.message.text
    try:
        a, b, c = map(float, userInput.split())
    except:
        await update.message.reply_text("Неправильный ввод, попробуйте еще раз", reply_markup=defaultkeyboard())
        return
    try:
        triangle = Triangle(a,b,c)
    except:
        await update.message.reply_text("Ошибка! Треугольник с данными сторонами не может существовать\nПопробуйте еще раз", reply_markup=defaultkeyboard())
    await update.message.reply_text("Треугольник создан успешно", reply_markup=defaultkeyboard())
async def sendMessage(message: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(message)

if __name__ == '__main__':
    application = ApplicationBuilder().token('7481543119:AAHwWVLmmJUh_JiStOD2Kz5s198kZ-DaylQ').build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~(filters.COMMAND), button_callback))
    
    application.run_polling()