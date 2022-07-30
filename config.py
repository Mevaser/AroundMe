import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    GOOGLE_KEY = os.environ.get('GOOGLE_KEY')