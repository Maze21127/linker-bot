from aiogram import types

from telegram.keyboards.default import MENU, get_keyboard
from telegram.loader import dp
from telegram.utils.messages import get_message


@dp.message_handler(lambda message: message.text in MENU['info'].values(), state="*")
async def start(message: types.Message):
    state = dp.current_state()
    await state.finish()

    user = message['from']
    await message.answer(get_message(user['language_code'], 'info'))


@dp.message_handler(lambda message: message.text in MENU['links'].values(), state="*")
async def start(message: types.Message):
    state = dp.current_state()
    await state.finish()

    user = message['from']
    await message.answer(get_message(user['language_code'], 'links'), reply_markup=get_keyboard(user['language_code'],
                                                                                                'links'))

