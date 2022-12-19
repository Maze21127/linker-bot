from aiogram import types
from aiogram.dispatcher import FSMContext

from logger import logger
from telegram.keyboards.default import LINKS, get_keyboard, CANCEL
from telegram.keyboards.inline.domain import get_domain_keyboard
from telegram.keyboards.inline.groups import get_groups_keyboard
from telegram.loader import dp, bot
from telegram.states.Links import CreateFreeLink, CreatePersonalLink
from telegram.states.Groups import CreateGroup, AddToGroup
from telegram.utils import api
from telegram.utils.api import check_access_link
from telegram.utils.database import create_link, LinkStatus, get_links, is_link_exist, get_groups, get_domain_for_group
from telegram.utils.links import is_correct
from telegram.utils.messages import get_message, get_domain_message


@dp.message_handler(lambda message: message.text in LINKS['show'].values(), state="*")
async def show(message: types.Message):
    state = dp.current_state()
    await state.finish()

    user = message['from']
    links = get_links(user['id'])
    groups = get_groups(user['id'])
    groups_message = "\n" + "\n".join([f"{i.name}\n" for i in groups]) if groups else None

    if not links:
        links_message = get_message(user['language_code'], 'no_links')
    else:
        links_message = "\n".join([f"{i.source}\n{i.domain_name}/{i.redirect} - {i.uses}\n" for i in links])
    result_message = get_message(user['language_code'], 'your_groups') + groups_message + "\n" + links_message \
        if groups_message is not None else links_message
    await message.answer(result_message, disable_web_page_preview=True)


@dp.message_handler(lambda message: message.text in LINKS['create'].values(), state="*")
async def start(message: types.Message):
    state = dp.current_state()
    await state.finish()

    user = message['from']
    await message.answer(get_message(user['language_code'], 'create'),
                         reply_markup=get_keyboard(user['language_code'], 'cancel'))
    await CreateFreeLink.waiting_source_url.set()


@dp.message_handler(lambda message: message.text in LINKS['buy'].values())
async def buy(message: types.Message):
    user = message['from']

    kb = get_domain_keyboard(False)
    await message.answer(get_message(user['language_code'], 'choose_domain'), reply_markup=kb)
    await CreatePersonalLink.waiting_domain.set()


@dp.message_handler(lambda message: message.text in LINKS['group'].values(), state="*")
async def group(message: types.Message):
    state = dp.current_state()
    await state.finish()

    user = message['from']
    kb = get_domain_keyboard(True)
    await message.answer(get_message(user['language_code'], 'choose_domain'), reply_markup=kb)
    await CreateGroup.waiting_domain.set()


@dp.callback_query_handler(state=[CreatePersonalLink.waiting_domain, CreateGroup.waiting_domain])
async def waiting_domain(callback_query: types. CallbackQuery, state: FSMContext):
    domain = callback_query.data
    user = callback_query.from_user
    await state.update_data(domain=domain)
    await bot.delete_message(user['id'], callback_query.message.message_id)
    await bot.send_message(user['id'],
                           get_domain_message(user['language_code'], domain),
                           reply_markup=get_keyboard(user['language_code'], 'cancel'))

    state_name = await state.get_state()

    if state_name == 'CreatePersonalLink:waiting_domain':
        return await CreatePersonalLink.waiting_redirect_url.set()
    elif state_name == 'CreateGroup:waiting_domain':
        logger.info("Now waiting_group_name state setting")
        return await CreateGroup.waiting_group_name.set()


@dp.message_handler(state=[CreatePersonalLink.waiting_redirect_url, CreateGroup.waiting_group_name])
async def waiting_redirect_url(message: types.Message, state: FSMContext):
    answer = message.text
    data = await state.get_data()
    domain = data.get("domain")

    user = message['from']
    language_code = user['language_code']
    if answer in CANCEL['cancel'].values():
        await state.finish()
        return await message.answer(get_message(language_code, 'links'),
                                    reply_markup=get_keyboard(language_code, 'links'))

    if len(answer) >= 25:
        return await message.answer(get_message(language_code, 'long_link'))

    if not is_correct(answer):
        return await message.answer(get_message(language_code, 'bad_link'))

    result = await api.check_link_existing(answer, domain)

    if result['status'] == 'already exist':
        logger.info(f"{answer} already exists")
        return await message.answer(get_message(language_code, 'already_exists'))

    state_name = await state.get_state()
    await state.update_data(redirect_url=answer)
    if state_name == 'CreatePersonalLink:waiting_redirect_url':
        await CreatePersonalLink.waiting_source_url.set()
        return await message.answer(get_message(language_code, 'create'),
                                    reply_markup=get_keyboard(language_code, 'links'))
    elif state_name == 'CreateGroup:waiting_group_name':
        if not is_correct(answer):
            return await message.answer(get_message(language_code, 'incorrect'),
                                        reply_markup=get_keyboard(language_code, 'links'))

        result = await api.create_group(answer, domain, user['id'])
        if result['status'] is LinkStatus.SUCCESS:
            success_message = get_message(language_code, 'group_created')
            await message.answer(f"{success_message}\n{result['link']}",
                                 reply_markup=get_keyboard(language_code, 'links'))
            await state.finish()
        #await CreateGroup.waiting_payment.set()
        #return await message.answer(get_message(message['from']['language_code'], 'payment_link'))


@dp.message_handler(state=CreateFreeLink.waiting_source_url)
async def waiting_free_source_url(message: types.Message, state: FSMContext):
    answer = message.text
    user = message['from']
    if answer in CANCEL['cancel'].values():
        await state.finish()
        return await message.answer(get_message(user['language_code'], 'links'),
                                    reply_markup=get_keyboard(user['language_code'], 'links'))

    if is_link_exist(answer):
        return await message.answer(get_message(message['from']['language_code'], 'already_exists'))

    if not await check_access_link(answer):
        return await message.answer(get_message(message['from']['language_code'], 'bad_link'))

    link = create_link(message['from']['id'], answer)
    result = await api.create_personal_link(source=answer, link=link, domain="qooby.ru")

    if result is LinkStatus.SUCCESS:
        await message.answer(f"http://qooby.ru/{link}", reply_markup=get_keyboard(user['language_code'], 'links'))

    await state.finish()


@dp.message_handler(state=CreatePersonalLink.waiting_source_url)
async def waiting_source_url(message: types.Message, state: FSMContext):
    answer = message.text
    user = message['from']
    if answer in CANCEL['cancel'].values():
        await state.finish()
        return await message.answer(get_message(user['language_code'], 'links'),
                                    reply_markup=get_keyboard(user['language_code'], 'links'))

    data = await state.get_data()
    redirect_link = data.get("redirect_url")
    domain = data.get("domain")

    if not await check_access_link(answer):
        return await message.answer(get_message(message['from']['language_code'], 'bad_link'))

    result = await api.create_personal_link(source=answer, link=redirect_link, domain=domain)

    if result is LinkStatus.SUCCESS:
        create_link(message['from']['id'], answer, redirect_link, domain=domain)
        await message.answer(f"Ссылка успешно куплена\n{domain}/{redirect_link}",
                             reply_markup=get_keyboard(user['language_code'], 'links'))
    elif result is LinkStatus.SOURCE_LINK_EXIST:
        return await message.answer(f"Такая ссылка уже существует",
                                    reply_markup=get_keyboard(user['language_code'], 'links'))
    elif result is LinkStatus.ERROR:
        await message.answer(f"Что-то пошло не так, попробуйте еще раз",
                             reply_markup=get_keyboard(user['language_code'], 'links'))

    await state.finish()


@dp.message_handler(lambda message: message.text in LINKS['menu'].values())
async def start(message: types.Message):
    user = message['from']
    return await message.answer(get_message(message['from']['language_code'], 'menu'),
                                reply_markup=get_keyboard(user['language_code'], 'menu'))


@dp.message_handler(lambda message: message.text in LINKS['add'].values(), state="*")
async def add(message: types.Message):
    state = dp.current_state()
    await state.finish()

    user = message['from']

    kb = get_groups_keyboard(user)
    if kb is None:
        return message.answer(get_message(user['language_code'], 'no_groups'))

    await message.answer(get_message(user['language_code'], 'choose_group'),
                         reply_markup=get_groups_keyboard(user))
    return await AddToGroup.waiting_group_name.set()


@dp.callback_query_handler(state=AddToGroup.waiting_group_name)
async def waiting_domain(callback_query: types. CallbackQuery, state: FSMContext):
    group_name = callback_query.data
    user = callback_query.from_user
    await state.update_data(group_name=group_name)
    await bot.delete_message(user['id'], callback_query.message.message_id)
    await bot.send_message(user['id'],
                           get_message(user['language_code'], 'link_name'),
                           reply_markup=get_keyboard(user['language_code'], 'cancel'))

    return await AddToGroup.waiting_link_name.set()


@dp.message_handler(state=AddToGroup.waiting_link_name)
async def waiting_source_url(message: types.Message, state: FSMContext):
    answer = message.text
    user = message['from']
    language_code = user['language_code']

    if answer in CANCEL['cancel'].values():
        await state.finish()
        return await message.answer(get_message(language_code, 'links'),
                                    reply_markup=get_keyboard(user['language_code'], 'links'))

    if len(answer) >= 25:
        return await message.answer(get_message(language_code, 'long_link'))

    await state.update_data(link_name=answer)
    await bot.send_message(user['id'],
                           get_message(user['language_code'], 'add_source'),
                           reply_markup=get_keyboard(user['language_code'], 'cancel'))

    return await AddToGroup.waiting_source_url.set()


@dp.message_handler(state=AddToGroup.waiting_source_url)
async def waiting_source_url(message: types.Message, state: FSMContext):
    answer = message.text
    user = message['from']
    language_code = user['language_code']

    if answer in CANCEL['cancel'].values():
        await state.finish()
        return await message.answer(get_message(language_code, 'links'),
                                    reply_markup=get_keyboard(user['language_code'], 'links'))

    if not await check_access_link(answer):
        return await message.answer(get_message(message['from']['language_code'], 'bad_link'))

    data = await state.get_data()
    link_name = data.get("link_name")
    group_name = data.get("group_name")

    domain = get_domain_for_group(group_name, user['id'])
    if domain['status'] is not LinkStatus.SUCCESS:
        return await message.answer("ERROR")

    result = await api.add_link_to_group(source=answer, link_name=link_name, domain=domain, group_name=group_name)

    if result is LinkStatus.SUCCESS:
        logger.info(f"{user['id']} добавил ссылку {link_name} в группу {group_name}")
        await message.answer(f"Ссылка успешно добавлена",
                             reply_markup=get_keyboard(user['language_code'], 'links'))
    elif result is LinkStatus.ERROR:
        await message.answer(f"Что-то пошло не так, попробуйте еще раз",
                             reply_markup=get_keyboard(user['language_code'], 'links'))
    await state.finish()
