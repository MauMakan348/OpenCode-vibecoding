class AppError(Exception):
    """Base error that routes translate into a JSON response."""

    status_code = 400

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ValidationError(AppError):
    status_code = 400


class NotFoundError(AppError):
    status_code = 404


class BusinessRuleError(AppError):
    status_code = 400
