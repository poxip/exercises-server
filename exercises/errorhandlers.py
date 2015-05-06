"""
    All error handlers used by API server
"""

class AbstractAPIError(Exception):
    """An abstract API error class"""
    error_code = -1  # Undefined error

    def __init__(self, message, status_code, payload=None):
        """Initialize API error instance
        :param str message: Error message
        :param int status_code: HTTP status code
        :param payload: HTTP payload
        """
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

        self.payload = payload

    def to_dict(self):
        """
        Serialize error data
        :return: A dictionary filled with serialized error's data
        """
        rv = dict(self.payload or ())
        rv['success'] = False
        rv['message'] = self.message
        rv['error'] = {
            'name': type(self).__name__,
            'code': self.error_code
        }

        return rv

class InvalidAPIUsage(AbstractAPIError):
    """API usage error"""
    status_code = 400
    error_code = 0

    def __init__(self, message, status_code=400, payload=None):
        AbstractAPIError.__init__(self, message, status_code, payload)

class DatabaseError(AbstractAPIError):
    """Server Database error"""
    status_code = 500
    error_code = 1

    def __init__(self, message, db_error, status_code=500, payload=None):
        """Initialize Database error instance
        :param str message: Error message
        :param sqlite3.Error db_error: SQLite3 error instance
        :param int status_code: HTTP status code
        :param payload: HTTP payload
        """
        AbstractAPIError.__init__(self, message, status_code, payload)
        self.db_error = db_error

    def to_dict(self):
        rv = AbstractAPIError.to_dict(self)
        rv['databaseError'] = "{0}: {1}".format(
            type(self.db_error).__name__,
            self.db_error.args[0]
        )

        return rv
