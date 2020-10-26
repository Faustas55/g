from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from HadesV2App import config
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://'+ config.username +":" + config.password +"@localhost/"+ config.database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



db = SQLAlchemy(app)

# This is the lazy mans version maybe I will add in the columns into the model
db.Model.metadata.reflect(db.engine)

from HadesV2App import routes
