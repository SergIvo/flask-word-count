import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'My_little_password'
    
    MAX_FILE_SIZE = 20971520
    UPLOAD_FOLDER = 'tmp'
    ALLOWED_EXTENSIONS = set(['txt'])
