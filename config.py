import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# Config
class Config():
    '''App configuration settings'''
    SECRET_KEY=os.getenv('SECRET_KEY')
    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_NOTIFICATIONS= False
    #max number of connections, adjust as needed
    SQLALCHEMY_POOL_SIZE=20
    #max number of seconds each connection lives, adjust as needed
    SQLALCHEMY_POOL_RECYCLE = 300

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    WTF_CSRF_ENABLED = False
