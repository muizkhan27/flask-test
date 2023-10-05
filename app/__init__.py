from . import routes  # This import is at the end to avoid circular imports
from flask import Flask
from flask_login import LoginManager
from config.secrets import SQLALCHEMY_DATABASE_URL
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    "SECRET_KEY"
] = "\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00"
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()

app.app_context().push()
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

db.init_app(app)
db.create_all()
