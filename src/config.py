from dotenv import load_dotenv
import os  # отдает нам значения переменных

load_dotenv()  # позволяет забрать данные из этого модуля

DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')

SECRET_AUTH = os.environ.get("SECRET_AUTH")
SMTP_USER = 'nerooren4001@gmail.com'
SMTP_PASSWORD = 'rhbb fhlu dsqm ilps'
