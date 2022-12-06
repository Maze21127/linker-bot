from . import domain


def get_cancel(language):
    return CANCEL[language] if language in CANCEL.keys() else CANCEL['en']


CANCEL = {
    "ru": "Отмена",
    "en": "Cancel"
}


