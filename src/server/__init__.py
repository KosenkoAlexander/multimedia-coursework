import os
from flask import Flask
from server.config import Config
from flask_login import LoginManager
from database.database import DatabaseConnector

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = os.getenv("POSTGRES_PASS", "postgres")
DB_HOST = "localhost"
db = DatabaseConnector(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST)

from server import routes

from server import user
