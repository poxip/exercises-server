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

@app.route('/question/<id>')
def question(id):
    """
    Get question data without solution
    :param id: Id of a question
    :return: question data without solution
    """
    if not id.isnumeric() or int(id) <= 0:
        raise InvalidAPIUsage("id must be an integer greater than 0")

    try:
        cur = g.db.execute(
            'SELECT title, content FROM questions WHERE id=?', id
        )
    except sqlite3.Error as e:
        raise DatabaseError("Database error", e)

    row = cur.fetchone()
    if row is None:
        raise ResourceNotFound("Question not found")

    return jsonify({
        'title': row[0],
        'content': row[1]
    })