"""
    API server resources
"""

import sqlite3

from flask.ext import restful
from flask.ext.restful import reqparse

from exercises import api, g
from exercises.errorhandlers import ErrorCode, \
    InvalidUsage, DatabaseError, ResourceNotFound
from exercises.helpers import normalize


class Question(restful.Resource):
    def get(self, question_id):
        """Get question data without solution

        :param question_id: Id of a question
        :return: question data without solution
        """
        if int(question_id) <= 0:
            raise InvalidUsage(
                "question_id must be an integer greater than 0",
                error_code=ErrorCode.WrongId
            )

        try:
            cur = g.db.execute(
                'SELECT title, content FROM questions WHERE id=?', (question_id,)
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

        return {
            'title': row[0],
            'content': row[1]
        }

class CheckQuestionAnswer(restful.Resource):
    def __init__(self):
        restful.Resource.__init__(self)
        self.arg_parser = reqparse.RequestParser()
        self.arg_parser.add_argument(
            'answer',
            type=str
        )

    def get(self, question_id):
        """Compare user's solution to solution in database

        :param int question_id: Question id
        :return Boolean: True if user's answer is correct, otherwise False
        """
        args = self.arg_parser.parse_args()

        answer = normalize(args.get('answer'))
        if int(question_id) <= 0:
            raise InvalidUsage(
                "question_id must be an integer greater than 0",
                error_code=ErrorCode.WrongId
            )

        if answer is '':
            raise InvalidUsage(
                "answer not set",
                error_code=ErrorCode.AnswerNotSet
            )

        try:
            cur = g.db.execute(
                'SELECT solution FROM questions WHERE id=?', (question_id,)
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

        solution = normalize(row[0])

        return {
            # @TODO: Improve answer checking
            'answerCorrect': answer == solution
        }

api.add_resource(Question, '/question/<int:question_id>')
api.add_resource(CheckQuestionAnswer, '/question/<int:question_id>/answer')