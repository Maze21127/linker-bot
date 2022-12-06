from os import getenv
from dotenv import load_dotenv


load_dotenv('.env')

# IP-Адресс базы данных PostgreSQL
DB_HOST = getenv('DB_HOST')
# Логин пользователя базы данных
DB_USER = getenv("DB_USER")
# Пароль пользователя базы данных
DB_PASSWORD = getenv("DB_PASSWORD")
# Имя базы данных
DB_NAME = getenv("DB_NAME")

AUTH_USERNAME = getenv('AUTH_USERNAME')
AUTH_KEY = getenv('AUTH_KEY')

SECRET_KEY = getenv('SECRET_KEY')
SALT = getenv('SALT')

DEV = True if getenv("DEV") == "True" else False


BOT_TOKEN = getenv('BOT_TOKEN')

BASIC_URL = getenv('BASIC_URL')
