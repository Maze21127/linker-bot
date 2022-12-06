from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from telegram.utils.database import get_domain_list


def get_domain_keyboard(group=True):
    domain_kb = InlineKeyboardMarkup()
    domain_list = get_domain_list()
    for domain in domain_list:
        domain_kb.add(InlineKeyboardButton(f"{domain.name}       {domain.price if not group else domain.group_price} ₽",
                                           callback_data=domain.name))
    return domain_kb


