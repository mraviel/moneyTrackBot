from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Constants import PSQL_KEY
from DatabaseCommands import DatabaseCommands


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app


# Configuration
app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = PSQL_KEY

db_command = DatabaseCommands(db)
