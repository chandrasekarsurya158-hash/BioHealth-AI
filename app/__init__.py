import os
from flask import Flask, render_template
from config import Config

def create_app(config_class=Config):
    """
    Application factory pattern.
    Creates and initializes the Flask application and registers all module blueprints.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Ensure all required upload directories exist
    upload_dirs = [
        app.config["PLANT_UPLOAD_FOLDER"],
        app.config["CROP_UPLOAD_FOLDER"],
        app.config["SKIN_UPLOAD_FOLDER"],
        app.config["XRAY_UPLOAD_FOLDER"],
        app.config["BLOOD_REPORT_FOLDER"],
    ]
    for directory in upload_dirs:
        os.makedirs(directory, exist_ok=True)
        
    # Register blueprints for all 17 pages across the 4 modules
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.agriculture import agri_bp
    from app.routes.medical import medical_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.admin import admin_bp
    from app.routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(agri_bp, url_prefix="/agriculture")
    app.register_blueprint(medical_bp, url_prefix="/medical")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(api_bp, url_prefix="/api/v1")
    
    # Global error handlers
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template("errors/403.html"), 403

    return app
