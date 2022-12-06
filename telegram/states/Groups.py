from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateGroup(StatesGroup):
    waiting_group_name = State()
    waiting_domain = State()
    waiting_payment = State()


class AddToGroup(StatesGroup):
    waiting_group_name = State()
    waiting_link_name = State()
    waiting_source_url = State()
