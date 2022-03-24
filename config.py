import os


class Config(object):
    SECRET_KEY ='j4td#+s3dHtzX'
    
    STORAGE_PATH = os.path.join(os.path.abspath("borkum-website"), "borkum\\website\\static")
