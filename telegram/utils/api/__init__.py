import aiohttp

from telegram.utils.database import LinkStatus, add_group

LINK_STATUSES = {
    'created': LinkStatus.SUCCESS,
    'already_exists': LinkStatus.SOURCE_LINK_EXIST,
    'error': LinkStatus.ERROR
}


async def check_link_existing(link: str, domain: str):
    async with aiohttp.ClientSession() as session:
        url = f"https://{domain}/api/v1/check_link/{link}"
        async with session.get(url) as resp:
            response = await resp.json()
            return response


async def create_group(group_name: str, domain: str, tg_id: int):
    async with aiohttp.ClientSession() as session:
        url = f"https://{domain}/api/v1/create_group/"
        data = {
            'group_name': group_name,
            'tg_id': tg_id
        }
        async with session.post(url, data=data) as resp:
            response = await resp.json()
            status = LINK_STATUSES[response['status']] if response['status'] in LINK_STATUSES.keys() \
                else LINK_STATUSES['error']
    if status is LinkStatus.SUCCESS:
        responce = add_group(tg_id, group_name, domain)
    else:
        responce = {"status": LinkStatus.ERROR}
    return responce


async def create_personal_link(source: str, link: str, domain: str):
    async with aiohttp.ClientSession() as session:
        url = f"https://{domain}/api/v1/create_link/"
        data = {
            'source': source,
            'link': link,
        }
        async with session.post(url, data=data) as resp:
            response = await resp.json()
            status = LINK_STATUSES[response['status']] if response['status'] in LINK_STATUSES.keys() \
                else LINK_STATUSES['error']
    if status is LinkStatus.SUCCESS:
        pass
    return status


async def add_link_to_group(source: str, link_name: str, domain: str, group_name: str):
    async with aiohttp.ClientSession() as session:
        url = f"https://{domain}/api/v1/add_link/"
        data = {
            'source': source,
            'link_name': link_name,
            'group_name': group_name,
        }
        async with session.post(url, data=data) as resp:
            response = await resp.json()
            status = LINK_STATUSES[response['status']] if response['status'] in LINK_STATUSES.keys() \
                else LINK_STATUSES['error']
    if status is LinkStatus.SUCCESS:
        pass
    return status


async def check_access_link(link: str):
    return link.startswith('https://')
    # async with aiohttp.ClientSession() as session:
    #     try:
    #         async with session.get(link, timeout=15) as resp:
    #             return resp.status in (200, 403)
    #     except aiohttp.client.InvalidURL:
    #         return False
