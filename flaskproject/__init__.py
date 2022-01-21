from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "mysecretkey123"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Admin@localhost/medico"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
UPLOAD_FOLDER = './static/uploads'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

from flaskproject import routes