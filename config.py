import os


class Config(object):
    SECRET_KEY ='j4td#+s3dHtzX'
    STORAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "borkum", "website", "static")
