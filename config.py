import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    STORAGE_PATH = os.path.join(basedir, "borkum", "website", "static")

    SQLALCHEMY_DATABASE_URI = f'sqlite:///{STORAGE_PATH}/database/data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
