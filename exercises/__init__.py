import sqlite3
from contextlib import closing

from flask import Flask, g, jsonify
from flask.ext import restful
from flask.ext.cors import CORS

from exercises.errorhandlers import AbstractError

# Create the application
app = Flask(__name__)
cors = CORS(app)
api = restful.Api(app)

# Setup configuration
if app.config.from_envvar('EXERCISES_CONFIG', silent=True) is not True:
    app.config.from_object('exercises.default_config')


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())

        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.errorhandler(AbstractError)
def handle_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code

    return response

import exercises.resources
