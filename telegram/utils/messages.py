def get_start_message(tg_user: dict) -> str:
    language = tg_user['language_code']
    if tg_user['first_name'] is not None:
        user = tg_user['first_name']
    elif tg_user['username'] is not None:
        user = tg_user['username']
    else:
        user = MESSAGES['user'][language] if language in MESSAGES['user'].keys() else MESSAGES['user']['en']
    message = MESSAGES['start'][language] if language in MESSAGES['start'].keys() else MESSAGES['start']['en']
    return message.replace('{USER}', user)


def get_message(language: str, message_type: str) -> str:
    return MESSAGES[message_type][language] if language in MESSAGES[message_type] else MESSAGES[message_type]['en']


def get_domain_message(language: str, domain: str):
    message = MESSAGES['after_domain'][language] if language in MESSAGES['after_domain'] else MESSAGES['after_domain'][
        'en']
    return message.replace("{DOMAIN}", domain)


start_ru = """
Привет {USER}, в этом боте ты сможешь бесплатно создать короткую ссылку или купить группу ссылок и личную именную ссылку.
"""

start_en = """
Hello {USER}, in this bot you can create short link for free or buy your group of links and personal link.
"""

links_ru = """
Здесь вы можете создать бесплатную ссылку, купить именную ссылку, купить свою группу ссылок, а так же увидеть статистику переходов по каждой ссылке.
<b>Стоимость именной ссылки - 1$</b>
"""

links_en = """
Here you can create free link, buy your personal link, create group of links or personal link and see statistics about any of your link.
<b>Price for personal link - 1$</b>
"""

after_domain_ru = """
Введите имя, которое будет после / 
www.{DOMAIN}/
"""

after_domain_en = """
Enter the name that will be after / 
www.{DOMAIN}/
"""

MESSAGES = {"user": {"ru": "Дружище",
                     "en": "Friend"},
            "info": {"ru": "Расскажу и покажу что может бот и как делать ссылки",
                     "en": "ENGLISH INFORMATION ABOUT BOT"},
            "start": {"ru": start_ru,
                      "en": start_en},
            'help': {"ru": 'help_ru',
                     "en": 'help_en'},
            "menu": {"ru": 'Меню',
                     'en': "Menu"},
            'links': {"ru": links_ru,
                      'en': links_en},
            'show': {"ru": "Ваши ссылки",
                     'en': "Your links"},
            'create': {"ru": "Введите исходную ссылку",
                       'en': "Input source link"},
            "choose_domain": {"ru": "Выберите домен",
                              "en": "Choose domain"},
            'choose_group': {"ru": "Выберите группу",
                             "en": "Choose group"},
            'no_groups': {"ru": "У вас еще нет ни одной группы",
                          "en": "You have not any group yet"},
            'buy': {"ru": "Введите ссылку, которую хотите купить",
                    'en': "Input link to buy"},
            'no_links': {"ru": "У вас нет ни одной ссылки",
                         'en': "You don't have any links"},
            'already_exists': {"ru": "Такая ссылка уже существует",
                               'en': "This url is already exists"},
            'after_domain': {"ru": after_domain_ru,
                             'en': after_domain_en},
            'payment_link': {"ru": "Ваша ссылка на оплату",
                             "en": "Your payment link"},
            'bad_link': {"ru": "Ссылка не работает",
                         "en": "Link is not work"},
            'long_link': {"ru": "Ссылка слишком длинная (больше 24 символов)",
                          "en": "Link is to long (more than 24 chars"},
            'group_created': {"ru": "Группа создана",
                              "en": "Group created"},
            'link_name': {"ru": "Введите название ссылки",
                          "en": "Enter link name"},
            'add_source': {"ru": "Введите ссылку, которую хотите добавить",
                           'en': "Enter link to add"},
            'incorrect': {"ru": "Недопустимое название",
                          "en": "Incorrect name"},
            'your_groups': {"ru": "Ваши группы",
                            "en": "Your groups"},
            'link_added_to_group': {"ru": "Ссылка добавлена в группу",
                                    "en": "Link added to group"}
            }
