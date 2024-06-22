import os


class Config(object):
    SECRET_KEY ='j4td#+s3dHtzX'
    STORAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "borkum", "website", "static")

    DB_PATH = f'{STORAGE_PATH}/database/'
    DB_NAME = 'borkum'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}/{DB_NAME}.db'
