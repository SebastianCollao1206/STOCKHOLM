import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a8f5f167f44f4964e6c998dee827110c'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:123456@localhost/STOCKHOLMDB2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
