"""
    API views
"""

import sqlite3

from flask import g, request, jsonify

from exercises import app
from exercises.errorhandlers import json_success, \
    ErrorCode, AbstractError, DatabaseError, InvalidUsage, ResourceNotFound


@app.errorhandler(AbstractError)
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
        raise InvalidUsage(
            "id must be an integer greater than 0",
            error_code=ErrorCode.IdNotInteger
        )

    try:
        cur = g.db.execute(
            'SELECT title, content FROM questions WHERE id=?', id
        )
    except sqlite3.Error as e:
        raise DatabaseError(
            "Database error",
            db_error=e,
            error_code=ErrorCode.DatabaseError
        )

    row = cur.fetchone()
    if row is None:
        raise ResourceNotFound(
            "Question not found",
            error_code=ErrorCode.QuestionNotFound
        )

    return json_success({
        'title': row[0],
        'content': row[1]
    })


@app.route('/question/answer/<id>', methods=['GET'])
def check_answer(id):
    """Check if the passed answer is correct

    Compare the answer passed through request to
    correct question's solution stored in database

    :param id: Id of a question
    """
    answer = request.args.get('answer', None)
    if not id.isnumeric() or int(id) <= 0:
        raise InvalidUsage(
            "id must be an integer greater than 0",
            error_code=ErrorCode.WrongId
        )

    if (answer is None) or (answer is ''):
        raise InvalidUsage(
            "answer not set",
            error_code=ErrorCode.AnswerNotSet
        )

    try:
        cur = g.db.execute(
            'SELECT solution FROM questions WHERE id=?', id
        )
    except sqlite3.Error as e:
        raise DatabaseError(
            "Database error",
            db_error=e,
            error_code=ErrorCode.DatabaseError
        )

    row = cur.fetchone()
    if row is None:
        raise ResourceNotFound(
            "question not found",
            error_code=ErrorCode.QuestionNotFound
        )

    answer_correct = True if answer is row[0] else False
    return json_success({
        'answerCorrect': answer_correct
    })