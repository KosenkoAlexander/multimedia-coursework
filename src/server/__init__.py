from flask import Flask
from server.config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from server import routes

from server import user
