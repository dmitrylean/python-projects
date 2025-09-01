import asyncio
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext

# 🔐 Загрузка переменных из .env
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

# 🤖 Инициализация бота
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# 📋 Клавиатура
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Оставить заявку")],
        [KeyboardButton(text="📁 Портфолио")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)

# 📦 Состояния формы
class OrderForm(StatesGroup):
    name = State()
    description = State()
    contact = State()

# 🏁 Команда /start с кнопками
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я фрилансер-бот. Выберите действие 👇",
        reply_markup=main_menu
    )

# 📤 Заявка
@dp.message(Command("order"))
async def start_order(message: Message, state: FSMContext):
    await message.answer("Как вас зовут?")
    await state.set_state(OrderForm.name)

@dp.message(OrderForm.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Опишите, что вам нужно:")
    await state.set_state(OrderForm.description)

@dp.message(OrderForm.description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Оставьте ваш контакт (телефон или Telegram username):")
    await state.set_state(OrderForm.contact)

@dp.message(OrderForm.contact)
async def process_contact(message: Message, state: FSMContext):
    data = await state.update_data(contact=message.text)
    await message.answer("Спасибо! Заявка получена ✅")

    text = (
        f"🆕 Новая заявка:\n\n"
        f"👤 Имя: {data['name']}\n"
        f"📄 Задача: {data['description']}\n"
        f"📞 Контакт: {data['contact']}"
    )
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
    await state.clear()

# 📁 Портфолио
@dp.message(Command("portfolio"))
async def cmd_portfolio(message: Message):
    await message.answer("Вот ссылка на моё портфолио: https://example.com")

# 💬 Обработка кнопок
@dp.message(lambda m: m.text == "📝 Оставить заявку")
async def handle_order_button(message: Message, state: FSMContext):
    await start_order(message, state)

@dp.message(lambda m: m.text == "📁 Портфолио")
async def handle_portfolio_button(message: Message):
    await cmd_portfolio(message)

# ℹ️ FAQ по ключевым словам
@dp.message(lambda m: "цены" in m.text.lower())
async def auto_faq(message: Message):
    await message.answer("Стоимость зависит от задачи. Напиши /order чтобы обсудить ✍️")

# 🚀 Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
