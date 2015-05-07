"""
    All error handlers used by API server
"""

from enum import IntEnum

class ErrorCode(IntEnum):
    """API server error codes"""
    UndefinedError = -1
    # InvalidUsage type
    WrongId = 10
    AnswerNotSet = 11
    # DatabaseError type
    DatabaseError = 20  # Covers all database errors
    # ResourceNotFound
    QuestionNotFound = 30


class AbstractError(Exception):
    """An abstract API error class"""

    def __init__(self, message, error_code=ErrorCode.UndefinedError,
                 status_code=None, payload=None):
        """Initialize API error instance
        :param str message: Error message
        :param ErrorCode error_code: API server error code
        :param int status_code: HTTP status code
        :param payload: HTTP payload
        """
        Exception.__init__(self)
        self.message = message
        self.error_code = error_code
        if status_code is not None:
            self.status_code = status_code

        self.payload = payload

    def to_dict(self):
        """
        Serialize error data
        :return: A dictionary filled with serialized error's data
        """
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['error'] = {
            'name': "{0}: {1}".format(
                type(self).__name__,
                self.error_code.name
            ),
            'code': self.error_code
        }

        return rv


class InvalidUsage(AbstractError):
    """API usage error"""
    status_code = 400


class DatabaseError(AbstractError):
    """Server Database error"""
    status_code = 500

    def __init__(self, message, db_error,
                 error_code=None, status_code=500, payload=None):
        """Initialize Database error instance
        :param str message: Error message
        :param sqlite3.Error db_error: SQLite3 error instance
        :param int status_code: HTTP status code
        :param payload: HTTP payload
        """
        AbstractError.__init__(self, message, error_code, status_code, payload)
        self.db_error = db_error

    def to_dict(self):
        rv = AbstractError.to_dict(self)
        rv['databaseError'] = "{0}: {1}".format(
            type(self.db_error).__name__,
            self.db_error.args[0]
        )

        return rv


class ResourceNotFound(AbstractError):
    status_code = 404
