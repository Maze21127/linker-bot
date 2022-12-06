from aiogram.dispatcher.filters.state import StatesGroup, State


class CreatePersonalLink(StatesGroup):
    waiting_domain = State()
    waiting_redirect_url = State()
    waiting_source_url = State()
    waiting_payment = State()


class CreateFreeLink(StatesGroup):
    waiting_source_url = State()
