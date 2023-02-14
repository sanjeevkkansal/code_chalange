import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./config.env")
basedir = os.path.abspath(os.path.dirname(__file__))

class DefaultConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = os.getenv('FLASK_ENV')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG')
    WX_DATA_FOLDER = os.getenv('WX_DATA_FOLDER')
    YLD_DATA_FILE = os.getenv('YLD_DATA_FILE')
    DATABASE_PATH = os.path.join(basedir, 'database.db')
    FLASK_PORT = os.getenv('FLASK_PORT')
    WX_DATA_FOLDER = os.path.join(os.path.dirname(__file__), "../wx_data")
    YLD_DATA_FILE = os.path.join(os.path.dirname(__file__), "../yld_data", "US_corn_grain_yield.txt")
