from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_keyboard(language: str, keyboard_type: str):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for key in KEYBOARDS[keyboard_type].keys():
        kb_lang = language if language in KEYBOARDS[keyboard_type][key].keys() else "en"
        if key == 'menu':
            keyboard.add(KeyboardButton(KEYBOARDS[keyboard_type][key][kb_lang]))
        else:
            keyboard.insert(KeyboardButton(KEYBOARDS[keyboard_type][key][kb_lang]))
    return keyboard


MENU = {'info': {"ru": "ℹ️ Информация",
                 'en': 'ℹ️ Info'},
        'links': {"ru": "Ссылки",
                  "en": "Links"},
        }

LINKS = {'show': {"ru": "Показать мои ссылки",
                  'en': 'Show my links'},
         'create': {"ru": "Создать ссылку",
                    "en": "Create new link"},
         'buy': {"ru": "Купить персональную ссылку",
                 'en': "Buy new personal link"},
         'group': {"ru": "Купить группу с ссылками",
                   "en": "Buy group with links"},
         'add': {"ru": "Добавить ссылку в группу",
                 "en": "Add link to group"},
         "menu": {"ru": "Вернуться в меню",
                  "en": "Back to main menu"}
         }

# FREE_LINKS = {
#
# }

CANCEL = {
    "cancel": {"ru": "Отмена",
               "en": "Cancel"}
}

KEYBOARDS = {"menu": MENU,
             "links": LINKS,
             'cancel': CANCEL}
