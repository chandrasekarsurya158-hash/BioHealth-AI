from flask import Blueprint, render_template, redirect, url_for

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    """Page 1: Home page."""
    return render_template("index.html")

@main_bp.route("/user/dashboard")
def user_dashboard_redirect():
    """Direct root redirect for /user/dashboard."""
    return redirect(url_for("dashboard.index"))

@main_bp.route("/about")
def about():
    """Page 2: About project page."""
    return render_template("about.html")

@main_bp.route("/api-docs")
def api_docs():
    """Page 18: Interactive Developer REST API v1 Reference."""
    return render_template("api_docs.html")

@main_bp.route("/emergency-directory")
def emergency_directory():
    """Page 19: National Emergency Helplines & Specialist Directory."""
    return render_template("directory.html")

@main_bp.route("/health-check")
def health_check():
    """System health check endpoint."""
    return {
        "status": "healthy",
        "system": "Multi-Domain AI Disease Detection & Intelligent Health Assistance",
        "phase": "Phase 2 - Complete Application Architecture & Frontend UI",
        "version": "2.0.0"
    }
