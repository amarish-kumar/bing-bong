from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
ctx = app.app_context()
with ctx:
	pass
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models
