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

# Loading boot from .env
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

# Bot initialization
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# Keyboard
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Submit a request")],
        [KeyboardButton(text="📁 Portfolio")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Select an action"
)

# Form States
class OrderForm(StatesGroup):
    name = State()
    description = State()
    contact = State()

# /start command with buttons
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Hi! I'm a freelance bot. Choose an action. 👇",
        reply_markup=main_menu
    )

# Application
@dp.message(Command("order"))
async def start_order(message: Message, state: FSMContext):
    await message.answer("What is your name?")
    await state.set_state(OrderForm.name)

@dp.message(OrderForm.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Describe what you need:")
    await state.set_state(OrderForm.description)

@dp.message(OrderForm.description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Leave your contact information (phone number or Telegram username):")
    await state.set_state(OrderForm.contact)

@dp.message(OrderForm.contact)
async def process_contact(message: Message, state: FSMContext):
    data = await state.update_data(contact=message.text)
    await message.answer("Thank you! Your request has been received. ✅")

    text = (
        f"🆕 New Order:\n\n"
        f"👤 Name: {data['name']}\n"
        f"📄 Task: {data['description']}\n"
        f"📞 Contact: {data['contact']}"
    )
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
    await state.clear()

# Portfolio
@dp.message(Command("portfolio"))
async def cmd_portfolio(message: Message):
    await message.answer("Portfolio: https://example.com")

# Button processing
@dp.message(lambda m: m.text == "📝 Submit A Request")
async def handle_order_button(message: Message, state: FSMContext):
    await start_order(message, state)

@dp.message(lambda m: m.text == "📁 Portfolio")
async def handle_portfolio_button(message: Message):
    await cmd_portfolio(message)

# Keyword FAQ
@dp.message(lambda m: "цены" in m.text.lower())
async def auto_faq(message: Message):
    await message.answer("The price depends on the task. Write /order to discuss ✍️")

# Start Bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
