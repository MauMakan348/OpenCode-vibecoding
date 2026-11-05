import os

from flask import Flask


def create_app(test_config=None):
    """Application factory for the Lab Equipment Loan System."""
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "lab_equipment.db"),
    )

    if test_config is not None:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    from app import database, errors
    from app.routes.item_routes import bp as item_blueprint
    from app.routes.loan_routes import bp as loan_blueprint

    database.init_app(app)
    errors.register_error_handlers(app)

    app.register_blueprint(item_blueprint)
    app.register_blueprint(loan_blueprint)

    return app
