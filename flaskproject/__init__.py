from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = "mysecretkey123"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Admin@localhost/medico"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

from flaskproject import routes