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


def register_error_handlers(app):
    """Return JSON for every handled error."""
    from flask import jsonify

    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({"error": error.message}), error.status_code

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def handle_internal_error(error):
        return jsonify({"error": "Internal server error"}), 500
