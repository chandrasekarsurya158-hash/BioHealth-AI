from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.admin import AdminModel
from app.models.user import UserModel
from app.models.db import test_connection
from app.utils.auth import admin_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    """Page 16: Admin authentication against MySQL admins or users table."""
    db_available = test_connection()

    if request.method == "POST":
        admin_key = request.form.get("admin_key", "").strip()
        password = request.form.get("password", "")

        if not admin_key or not password:
            flash("Administrator username/email and password required.", "danger")
            return render_template("admin/login.html", db_available=db_available)

        if not db_available:
            flash("Admin authentication requires a connected database. This demo deployment does not have a persistent database configured.", "warning")
            return render_template("admin/login.html", db_available=db_available)

        try:
            # 1. Try admins table first
            admin = AdminModel.get_by_username(admin_key)
            if not admin and "@" in admin_key:
                # Try finding in users table with role='admin'
                user_admin = UserModel.get_by_email(admin_key)
                if user_admin and user_admin.get("role") == "admin":
                    admin = {
                        "id": user_admin["id"],
                        "username": user_admin["email"],
                        "fullname": user_admin["fullname"],
                        "email": user_admin["email"],
                        "password_hash": user_admin["password_hash"]
                    }

            if admin and AdminModel.verify_password(admin["password_hash"], password):
                session.clear()
                session["admin_logged_in"] = True
                session["admin_id"] = admin["id"]
                session["admin_name"] = admin["fullname"]
                session["role"] = "admin"

                AdminModel.log_activity(
                    admin_id=admin["id"],
                    admin_name=admin["fullname"],
                    action="LOGIN",
                    target_module="AUTHENTICATION",
                    details=f"Admin {admin['fullname']} logged in successfully.",
                    ip_address=request.remote_addr
                )

                flash(f"Administrator access granted: Welcome, {admin['fullname']}.", "success")
                return redirect(url_for("admin.dashboard"))
            else:
                flash("Invalid administrator credentials.", "danger")
        except Exception as e:
            flash(f"Authentication error: {str(e)}", "danger")

    return render_template("admin/login.html", db_available=db_available)

@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    """Page 17: Admin management console with real database aggregate metrics and model monitoring."""
    try:
        analytics = AdminModel.get_system_analytics()
    except Exception:
        analytics = {
            "total_users": 0,
            "total_scans": 0,
            "plant_scans": 0,
            "crop_scans": 0,
            "skin_scans": 0,
            "xray_scans": 0,
            "blood_scans": 0,
            "symptoms_scans": 0,
            "total_medicines": 0
        }

    # Live Model Status Checks
    from app.models.plant_classifier import PlantClassifier
    from app.models.crop_classifier import CropClassifier
    from app.models.skin_classifier import SkinClassifier
    from app.models.xray_classifier import XrayClassifier

    models_status = {
        "plant": PlantClassifier.is_model_available(),
        "crop": CropClassifier.is_model_available(),
        "skin": SkinClassifier.is_model_available(),
        "xray": XrayClassifier.is_model_available(),
        "blood": True,     # PyMuPDF Document OCR Parser
        "symptoms": True   # Evidence-based Clinical Triage Engine
    }

    try:
        recent_logs = AdminModel.get_recent_logs(limit=10)
    except Exception:
        recent_logs = []

    return render_template(
        "admin/dashboard.html", 
        analytics=analytics, 
        models_status=models_status,
        recent_logs=recent_logs
    )

@admin_bp.route("/users")
@admin_required
def user_management():
    """Admin User Management Console."""
    try:
        users_list = UserModel.get_all_users()
    except Exception:
        users_list = []
    return render_template("admin/users.html", users=users_list)

@admin_bp.route("/users/<int:user_id>/role", methods=["POST"])
@admin_required
def update_user_role(user_id):
    """Change authorization role of a user."""
    new_role = request.form.get("role", "user")
    if UserModel.update_user_role(user_id, new_role):
        admin_name = session.get("admin_name", "Admin")
        AdminModel.log_activity(
            admin_id=session.get("admin_id"),
            admin_name=admin_name,
            action="UPDATE_ROLE",
            target_module="USER_MANAGEMENT",
            details=f"Updated User #{user_id} role to '{new_role}'.",
            ip_address=request.remote_addr
        )
        flash(f"User #{user_id} role updated to '{new_role}'.", "success")
    else:
        flash("Could not update user role.", "danger")
    return redirect(url_for("admin.user_management"))

@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def delete_user(user_id):
    """Permanently delete a user account and associated scans."""
    admin_id = session.get("admin_id")
    if user_id == admin_id:
        flash("You cannot delete your own active administrator account.", "warning")
        return redirect(url_for("admin.user_management"))

    try:
        UserModel.delete_account(user_id)
        AdminModel.log_activity(
            admin_id=admin_id,
            admin_name=session.get("admin_name", "Admin"),
            action="DELETE_USER",
            target_module="USER_MANAGEMENT",
            details=f"Permanently purged User #{user_id} and all scan records.",
            ip_address=request.remote_addr
        )
        flash(f"User #{user_id} permanently removed.", "info")
    except Exception as e:
        flash(f"Error deleting user: {e}", "danger")

    return redirect(url_for("admin.user_management"))

@admin_bp.route("/medicines")
@admin_required
def medicine_management():
    """Admin Medicine & Pharmacopeia Management Console."""
    try:
        medicines = AdminModel.get_all_medicines()
    except Exception:
        medicines = []
    return render_template("admin/medicines.html", medicines=medicines)

@admin_bp.route("/medicines/add", methods=["POST"])
@admin_required
def add_medicine():
    """Add a verified medicine to the system database."""
    name = request.form.get("name", "").strip()
    generic_name = request.form.get("generic_name", "").strip()
    brand_examples = request.form.get("brand_examples", "").strip()
    category = request.form.get("category", "").strip()
    prescription_type = request.form.get("prescription_type", "OTC")
    uses = request.form.get("uses", "").strip()
    precautions = request.form.get("precautions", "").strip()
    warnings = request.form.get("warnings", "").strip()
    side_effects = request.form.get("side_effects", "").strip()
    contraindications = request.form.get("contraindications", "").strip()

    if not name or not generic_name or not category or not uses:
        flash("Name, Generic Name, Category, and Therapeutic Uses are required.", "warning")
        return redirect(url_for("admin.medicine_management"))

    try:
        AdminModel.add_medicine(
            name, generic_name, brand_examples, category, prescription_type, 
            uses, precautions, warnings, side_effects, contraindications
        )
        AdminModel.log_activity(
            admin_id=session.get("admin_id"),
            admin_name=session.get("admin_name", "Admin"),
            action="ADD_MEDICINE",
            target_module="PHARMACOPEIA",
            details=f"Added medicine record: '{name}' ({prescription_type}).",
            ip_address=request.remote_addr
        )
        flash(f"Medicine '{name}' successfully registered into verified database.", "success")
    except Exception as e:
        flash(f"Error adding medicine: {e}", "danger")

    return redirect(url_for("admin.medicine_management"))

@admin_bp.route("/medicines/<int:med_id>/delete", methods=["POST"])
@admin_required
def delete_medicine(med_id):
    """Delete a medicine record from the database."""
    try:
        AdminModel.delete_medicine(med_id)
        AdminModel.log_activity(
            admin_id=session.get("admin_id"),
            admin_name=session.get("admin_name", "Admin"),
            action="DELETE_MEDICINE",
            target_module="PHARMACOPEIA",
            details=f"Deleted medicine ID #{med_id}.",
            ip_address=request.remote_addr
        )
        flash(f"Medicine record #{med_id} deleted.", "info")
    except Exception as e:
        flash(f"Error deleting medicine: {e}", "danger")

    return redirect(url_for("admin.medicine_management"))

@admin_bp.route("/logs")
@admin_required
def system_logs():
    """System activity audit log viewer."""
    try:
        logs = AdminModel.get_recent_logs(limit=50)
    except Exception:
        logs = []
    return render_template("admin/logs.html", logs=logs)

@admin_bp.route("/logout")
def logout():
    """Admin logout action."""
    admin_name = session.get("admin_name", "Admin")
    admin_id = session.get("admin_id")
    if admin_id:
        AdminModel.log_activity(
            admin_id=admin_id,
            admin_name=admin_name,
            action="LOGOUT",
            target_module="AUTHENTICATION",
            details=f"Admin {admin_name} ended their session.",
            ip_address=request.remote_addr
        )
    session.clear()
    flash("Administrator session safely terminated.", "info")
    return redirect(url_for("admin.login"))
