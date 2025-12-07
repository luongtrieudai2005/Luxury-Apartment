from flask import Flask
from .config import DevConfig
from .extensions.db import init_app as init_db


def create_app(config_object=DevConfig):
    app = Flask(
        __name__,
        template_folder=config_object.TEMPLATE_FOLDER,
        static_folder=config_object.STATIC_FOLDER,
    )
    app.config.from_object(config_object)

    # extensions
    init_db(app)

    # blueprints
    from .route.auth import bp as auth_bp
    from .route.main import bp as main_bp
    from .route.core import bp as core_bp
    from .route.iot import bp as iot_bp, api as iot_api_bp
    from .route.reports import bp as reports_bp
    from .route.admin import bp as admin_bp
    from .route.support import bp as support_bp
    from .route.profile import bp as profile_bp
    
    app.register_blueprint(profile_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(core_bp)
    app.register_blueprint(iot_bp)
    app.register_blueprint(iot_api_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(support_bp)


    return app
