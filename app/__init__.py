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
    
    # Ensure all required upload directories exist (guarded for read-only serverless filesystems)
    upload_dirs = [
        app.config.get("PLANT_UPLOAD_FOLDER"),
        app.config.get("CROP_UPLOAD_FOLDER"),
        app.config.get("SKIN_UPLOAD_FOLDER"),
        app.config.get("XRAY_UPLOAD_FOLDER"),
        app.config.get("BLOOD_REPORT_FOLDER"),
    ]
    for directory in upload_dirs:
        if directory:
            try:
                os.makedirs(directory, exist_ok=True)
            except OSError:
                # Read-only filesystem in cloud serverless environments (e.g., Vercel)
                pass
        
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

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("errors/500.html"), 500

    return app
