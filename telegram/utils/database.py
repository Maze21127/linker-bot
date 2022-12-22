import random
from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from logger import logger
from settings import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, BASIC_URL

import string

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

Base = declarative_base()


class LinkStatus(Enum):
    SUCCESS = 'created'
    SOURCE_LINK_EXIST = 'source link exists'
    ERROR = "error"


class TgUser(Base):
    __tablename__ = "tg_user"

    tg_id = Column(BigInteger, primary_key=True)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))

    urls = relationship('Url', back_populates='users')


class Url(Base):
    __tablename__ = "url"

    id = Column(Integer, primary_key=True)
    redirect = Column(String(255), nullable=False, unique=True)
    source = Column(Text, nullable=False, unique=True)
    uses = Column(Integer, default=0)
    user_id = Column(BigInteger, ForeignKey("tg_user.tg_id"))
    group_id = Column(Integer, ForeignKey("url_group.id"))
    domain_id = Column(BigInteger, ForeignKey('url_domain.id'), default=1)

    users = relationship('TgUser', back_populates='urls')
    domains = relationship('Group', back_populates='urls_')


class Group(Base):
    __tablename__ = "url_group"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    user_id = Column(BigInteger, ForeignKey('tg_user.tg_id'))
    domain_id = Column(BigInteger, ForeignKey('url_domain.id'))

    urls_ = relationship('Url', back_populates='domains')


class Domain(Base):
    __tablename__ = "url_domain"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    group_price = Column(Integer, nullable=False)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()


def add_user(user: dict):
    tg_user = TgUser(tg_id=user['id'], username=user['username'], first_name=user['first_name'], last_name=user['last_name'])
    if session.query(TgUser).filter(TgUser.tg_id == tg_user.tg_id).first() is None:
        session.add(tg_user)
        session.commit()
        logger.info(f"{tg_user.tg_id} добавлен")


async def is_personal_link_exist(redirect: str):
    return session.query(Url).filter(Url.redirect == redirect).first() is not None


def is_link_exist(source: str):
    return session.query(Url).filter(Url.source == source).first() is not None


def create_link(tg_id: int, source: str, redirect: None | str = None, domain='qooby.ru'):
    if redirect is None:
        link = _generate_url()
        return link
    else:
        link = redirect
    domain_id = session.query(Domain).filter(Domain.name == domain).first()
    checking = session.query(Url).filter(Url.source == source, Url.domain_id == domain_id.id, Url.redirect == redirect).first()
    if checking:
        return {"status": LinkStatus.SOURCE_LINK_EXIST, "link": f"{BASIC_URL}/{link}"}
    url = Url(source=source, redirect=link, user_id=tg_id, domain_id=domain_id.id)
    session.add(url)
    session.commit()
    logger.info(f"{source}\n{link} добавлен")
    return {"status": LinkStatus.SUCCESS, "link": f"{BASIC_URL}/{link}"}


def add_group(tg_id: int, group_name: str, domain_name: str):
    try:
        domain = session.query(Domain).filter(Domain.name == domain_name).first()

        group = Group(name=group_name, user_id=tg_id, domain_id=domain.id)
        session.add(group)
        session.commit()
        logger.info(f"{group.name} создана пользователей {group.user_id} на домене {group.domain_id}")
        return {"status": LinkStatus.SUCCESS, "link": f"{domain.name}/{group_name}"}
    except Exception as ex:
        logger.exception(ex)
        return {"status": LinkStatus.ERROR}


def get_domain_for_group(group_name: str, tg_id: int):
    try:
        domain_id = session.query(Group).filter(Group.name == group_name, Group.user_id == tg_id).first().domain_id
        domain = session.query(Domain).filter(Domain.id == domain_id).first().name
        return {"status": LinkStatus.SUCCESS, "domain": domain}
    except Exception as ex:
        logger.exception(ex)
        return {"status": LinkStatus.ERROR}


def get_groups(tg_id: int) -> list[Group]:
    groups = session.query(Group).filter(Group.user_id == tg_id).all()
    return sorted(groups, key=lambda x: x.id)


def get_links(tg_id: int) -> list:
    links = session.query(TgUser).where(TgUser.tg_id == tg_id).one().urls
    if len(links) == 0:
        return []

    domains = session.query(Domain).all()

    for link in links:
        for domain in domains:
            if link.domain_id == domain.id:
                link.domain_name = domain.name
    return sorted(links, key=lambda x: x.id)


def _generate_url():
    alphabet = string.ascii_lowercase + '0123456789' + string.ascii_uppercase
    LENGTH = 6
    while True:
        link = "".join([random.choice(alphabet) for _ in range(LENGTH)])
        if not is_link_exist(link):
            return link


def get_domain_list():
    return session.query(Domain).all()


def get_group_list(tg_id: int):
    return session.query(Group).filter_by(user_id=tg_id).all()
