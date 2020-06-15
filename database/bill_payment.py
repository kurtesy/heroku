from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import dev

app = Flask(dev.APP_NAME)
db = SQLAlchemy(app)


