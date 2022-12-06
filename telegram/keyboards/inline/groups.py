from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from telegram.keyboards.inline import get_cancel
from telegram.utils.database import get_group_list


def get_groups_keyboard(user):
    group_kb = InlineKeyboardMarkup()
    tg_id = user.id
    lang_code = user.language_code

    group_list = get_group_list(tg_id)

    if len(group_list) == 0:
        return None

    for group in group_list:
        group_kb.add(InlineKeyboardButton(f"{group.name}", callback_data=group.name))
    group_kb.add(InlineKeyboardButton(get_cancel(lang_code), callback_data="cancel"))

    return group_kb


