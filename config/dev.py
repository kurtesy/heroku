"""
Development environment config
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
ENV = "development"
SECRET_KEY = "ABCD"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,  'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'setu_db_repo')
APP_NAME = 'SetuApp'
APP_API_KEY = 'kaJsa873knGHQ'