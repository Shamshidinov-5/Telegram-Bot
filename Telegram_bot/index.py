
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# Initialize logging
logging.basicConfig(level=logging.INFO)

# Bot token
API_TOKEN = '7232171935:AAEG-Il34oRIH-76sQyMRTt_ko0D4fjp3jI'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Define states
class Form(StatesGroup):
    role = State()
    name = State()
    age = State()
    technology = State()
    telegram = State()
    contact = State()
    location = State()
    price = State()
    availability = State()
    goal = State()

# Main menu buttons
main_buttons = [
    KeyboardButton('📋 Tariflar'),
    KeyboardButton('📢 Reklama')
]
main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(*main_buttons)

# Tarif buttons
tarif_buttons = [
    KeyboardButton('🪪 Rezyume'),
    KeyboardButton('📄 Vakansiya'),
    KeyboardButton('📰 Advertisement'),
    KeyboardButton('Ortga')
]
tarif_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(*tarif_buttons)

# Reklama buttons
reklama_buttons = [
    KeyboardButton('Ustoz'),
    KeyboardButton('Shogird'),
    KeyboardButton('Sherik'),
    KeyboardButton('Xodim'),
    KeyboardButton('Ish joyi'),
    KeyboardButton('O\'quv kursi'),
    KeyboardButton('Ortga')
]



reklama_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(*reklama_buttons)


@dp.message_handler(Text(equals=['Ustoz', 'Shogird', 'Sherik', 'Xodim', 'Ish joyi', 'O\'quv kursi', 'Ortga']))
async def reklama_form(message: types.Message):
    if message.text == 'Ortga':
        await message.answer("Asosiy menyuga qaytdiz:", reply_markup=main_menu)
    else:
        await message.answer("Reklama uchun ma'lumotlar to'plangan.")



# Submenu buttons for Tarif categories
resume_tarifs = [
    KeyboardButton('🆓 Bepul ta\'rif'),
    KeyboardButton('🆕 Pullik ta\'rif - 5000 so‘m'),
    KeyboardButton('Ortga')
]
vacancy_tarifs = [
    KeyboardButton('🆙 Standard ta\'rif - 5000 so‘m'),
    KeyboardButton('🆕 Foydali ta\'rif - 9000 so‘m'),
    KeyboardButton('🆒 Natijaviy ta\'rif - 11000 so‘m'),
    KeyboardButton('Ortga')
]
advert_tarifs = [
    KeyboardButton('🆙 Standard ta\'rif - 10000 so‘m'),
    KeyboardButton('🆕 Foydali ta\'rif - 17000 so‘m'),
    KeyboardButton('*⃣ Tungi ta\'rif - 23000 so‘m'),
    KeyboardButton('🔀 Oylik ta‘rif - 39000 so‘m'),
    KeyboardButton('Ortga')
]
resume_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(*resume_tarifs)
vacancy_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(*vacancy_tarifs)
advert_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(*advert_tarifs)

# Define payment methods inline keyboard
payment_buttons = [
    InlineKeyboardButton("Humo", callback_data='payment_humo'),
    InlineKeyboardButton("Uzcard", callback_data='payment_uzcard')
]
payment_menu = InlineKeyboardMarkup().add(*payment_buttons)

# Start command handler
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    description = (
        "Salom! Men ReklamaTarifBotman. Bu bot orqali turli tariflar va reklama imkoniyatlarini ko'rishingiz mumkin.\n\n"
        "Quyidagi bo'limlardan birini tanlang:\n"
        "- 📋 Tariflar: Rezyume, Vakansiya yoki Advertisement tariflarini ko'rish.\n"
        "- 📢 Reklama: O'z reklamangizni joylashtirish."
    )
    await message.answer(description, reply_markup=main_menu)

# Main menu handler
@dp.message_handler(Text(equals=['📋 Tariflar', '📢 Reklama']))
async def show_main_submenus(message: types.Message):
    if message.text == '📋 Tariflar':
        await message.answer("Tarif bo'limini tanlang:", reply_markup=tarif_menu)
    elif message.text == '📢 Reklama':
        await message.answer("Reklama bo'limini tanlang:", reply_markup=reklama_menu)

# Tarif categories handler
@dp.message_handler(Text(equals=['🪪 Rezyume', '📄 Vakansiya', '📰 Advertisement']))
async def show_tarif_menu(message: types.Message):
    if message.text == '🪪 Rezyume':
        await message.answer("Rezyume tariflarini tanlang:", reply_markup=resume_menu)
    elif message.text == '📄 Vakansiya':
        await message.answer("Vakansiya tariflarini tanlang:", reply_markup=vacancy_menu)
    elif message.text == '📰 Advertisement':
        await message.answer("Reklama tariflarini tanlang:", reply_markup=advert_menu)

# Updated Tarif details handler
@dp.message_handler(Text(startswith=['🆓', '🆕', '🆙', '🆒', '*⃣', '🔀']))
async def show_tarif_details(message: types.Message):
    tarif_details = {
        '🆓 Bepul ta\'rif': "● e‘lon 24 soat ichida kanalga joylanadi\n● e‘lon 1 soat topda turadi.",
        '🆕 Pullik ta\'rif - 5000 so‘m': "● e‘lon 4 soat ichida kanalga joylanadi\n● e‘lon 2 soat topda turadi.",
        '🆙 Standard ta\'rif - 5000 so‘m': "● e‘lon 24 soat ichida kanalga joylanadi\n● e‘lon 1 soat topda turadi.",
        '🆕 Foydali ta\'rif - 9000 so‘m': "● e‘lon 4 soat ichida kanalga joylanadi\n● e‘lon 2 soat topda turadi.",
        '🆒 Natijaviy ta\'rif - 11000 so‘m': "● e‘lon 1 soat ichida kanalga joylanadi\n● e‘lon 3 soat topda turadi\n● agar joylangan e‘lon foyda bermasa yana 1 marta bepul joylab beriladi.",
        '🆙 Standard ta\'rif - 10000 so‘m': "● e‘lon 24 soat ichida kanalga joylanadi\n● e‘lon 1 soat topda turadi.",
        '🆕 Foydali ta\'rif - 17000 so‘m': "● e‘lon 4 soat ichida kanalga joylanadi\n● e‘lon 2 soat topda turadi.",
        '*⃣ Tungi ta\'rif - 23000 so‘m': "● e‘lon 24 soat ichida kanalga joylanadi\n● e‘lon tungi soat 23:00 dan ertalab 9:00 gacha topda turadi.",
        '🔀 Oylik ta‘rif - 39000 so‘m': "● 1 oyda 5 martagacha e‘lon joylash imkoniyati\n● e‘lon 2 soat ichida kanalga joylanadi\n● e‘lon 2 soat topda turadi."
    }

    # Creating selection buttons
    selection_buttons = [
        InlineKeyboardButton('Tanlash', callback_data='select'),
        InlineKeyboardButton('Ortga', callback_data='back')
    ]
    selection_menu = InlineKeyboardMarkup(row_width=2).add(*selection_buttons)
    
    await message.answer(
        tarif_details.get(message.text, "Noma'lum tarif."),
        reply_markup=selection_menu
    )


@dp.callback_query_handler(lambda c: c.data == 'back')
async def select_tarif(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.answer("Ortga qaytdizngiz:", reply_markup=main_menu)  # main_menu ni ishlatish


# Selection handler
@dp.callback_query_handler(lambda c: c.data == 'select')
async def select_tarif(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.answer("Tarif tanlandi! Iltimos, to'lov usulini tanlang:", reply_markup=payment_menu)

# Callback handler for payment methods
@dp.callback_query_handler(lambda c: c.data in ['payment_humo', 'payment_uzcard'])
async def process_payment(callback_query: types.CallbackQuery):
    payment_method = "Humo" if callback_query.data == 'payment_humo' else "Uzcard"
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Siz {payment_method} to'lov usulini tanladingiz!")

# Reklama form handling
@dp.message_handler(Text(equals=['Ustoz', 'Shogird', 'Sherik', 'Xodim', 'Ish joyi', 'O\'quv kursi']))
async def reklama_form(message: types.Message):
    # Your form handling logic here
    await message.answer("Reklama uchun ma'lumotlar to'plangan.")

# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)










