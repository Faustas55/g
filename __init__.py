from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/hades.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



db = SQLAlchemy(app)

# This is the lazy mans version maybe I will add in the columns into the model
db.Model.metadata.reflect(db.engine)

from HadesV2App import routes
