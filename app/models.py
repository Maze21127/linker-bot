from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(session_options={"autoflush": False})


class TgUser(db.Model):
    __tablename__ = 'tg_user'

    tg_id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))

    def __init__(self, tg_id: int, username: str, first_name: str, last_name: str):
        self.tg_id = tg_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    def json(self):
        return {
            "tg_id": self.tg_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }


class Payment(db.Model):
    __tablename__ = 'payment_request'

    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.String(255), nullable=False)
    tg_id = db.Column(db.BigInteger, db.ForeignKey("tg_user.tg_id"))
    event = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime)
    label = db.Column(db.String(255))
    status = db.Column(db.String(255))
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, payment_id: str, tg_id: int, event: str, timestamp, label: str, status: str, price: int):
        self.payment_id = payment_id
        self.tg_id = tg_id
        self.event = event
        self.timestamp = timestamp
        self.label = label
        self.status = status
        self.price = price

    def json(self):
        return {
            "payment_id": self.payment_id,
            "tg_id": self.tg_id,
            "event": self.event,
            "timestamp": self.timestamp,
            "label": self.label,
            "status": self.status,
            "price": self.price
        }


class Url(db.Model):
    __tablename__ = 'url'

    id = db.Column(db.Integer, primary_key=True)
    redirect = db.Column(db.String(25), nullable=False)
    source = db.Column(db.Text)
    uses = db.Column(db.Integer, default=0)
    user_id = db.Column(db.BigInteger, db.ForeignKey("tg_user.tg_id"))
    group_id = db.Column(db.Integer)
    domain_id = db.Column(db.BigInteger, db.ForeignKey('url_domain.id'), default=1)

    def __init__(self, tg_id: int, redirect: str, source: str, user_id: int, group_id: int| None, uses: int = 0,
                 domain_id: int = 0):
        self.tg_id = tg_id
        self.redirect = redirect
        self.source = source
        self.user_id = user_id
        self.group_id = group_id
        self.uses = uses
        self.domain_id = domain_id

    def json(self):
        return {
            "ip_address": self.ip_address,
            "number_of_users": self.number_of_users,
            "bot_name": self.bot_name
        }


class Domain(db.Model):
    __tablename__ = "url_domain"

    id = db.Column(db.Integer, primary_key=True)
    redirect = db.Column(db.String(255), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)

