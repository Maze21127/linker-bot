from flask import Flask
from app import utils
from settings import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, SECRET_KEY


app = Flask(__name__)
app.secret_key = SECRET_KEY

app.jinja_env.globals.update(get_correct_transfer_string=utils.get_correct_transfer_string)
app.jinja_env.globals.update(remove_port_from_ip=utils.remove_port_from_ip)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


from app import views
