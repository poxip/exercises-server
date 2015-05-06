"""
    API views
"""

import sqlite3

from exercises import app, g
from exercises.errorhandlers \
    import AbstractAPIError, DatabaseError, InvalidAPIUsage, ResourceNotFound

from flask import jsonify

@app.errorhandler(AbstractAPIError)
def handle_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code

    return response

