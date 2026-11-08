import os
from dotenv import load_dotenv
load_dotenv('.env')

class Config(object):
    USER = os.environ.get('POSTGRESQL_USER', )
    PASSWORD = os.environ.get('POSTGRESQL_PASSWORD', )
    HOST = os.environ.get('POSTGRESQL_HOST', 'localhost')
    PORT = os.environ.get('POSTGRESQL_PORT', '5432')
    DB = os.environ.get('POSTGRESQL_DB', 'timreverseDB')

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')




