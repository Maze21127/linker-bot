from aiogram import types

from telegram.keyboards.default import get_keyboard
from telegram.loader import dp
from telegram.utils.database import add_user

from telegram.utils.messages import get_start_message


@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message):
    state = dp.current_state()
    await state.finish()

    user = message['from']
    add_user(user)
    return await message.answer(get_start_message(user), reply_markup=get_keyboard(user['language_code'], 'menu'))


