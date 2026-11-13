import time
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.models.user import UserModel
from app.models.db import get_db
from app.utils.auth import login_required

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@dashboard_bp.route("/user/dashboard")
@login_required
def index():
    """Page 5: User dashboard with real database scan counters."""
    user_id = session.get("user_id")
    user_name = session.get("user_name", "User")
    
    try:
        counts = UserModel.get_dashboard_counts(user_id)
    except Exception:
        counts = {"plant": 0, "crop": 0, "skin": 0, "blood": 0, "xray": 0, "symptoms": 0, "total": 0}
        
    return render_template("dashboard/index.html", user_name=user_name, counts=counts)

@dashboard_bp.route("/user/dashboard", endpoint="user_dashboard")
@login_required
def user_dashboard():
    """Alias endpoint for /user/dashboard redirect compatibility."""
    return index()

@dashboard_bp.route("/results")
def results():
    """
    Page 13: Detection and assessment results page.
    Accessible to both logged-in users and guests who just ran a scan.
    """
    module = request.args.get("module", "plant")
    analysis = session.get("last_analysis")

    if analysis and isinstance(analysis, dict) and analysis.get("module") == "symptoms":
        from app.models.symptoms_analyzer import GLOBAL_ASSESSMENT_CACHE
        report_id = analysis.get("report_id")
        # Hydrate from server-side memory store
        if report_id and report_id in GLOBAL_ASSESSMENT_CACHE:
            analysis = {**analysis, **GLOBAL_ASSESSMENT_CACHE[report_id]}
        elif "latest" in GLOBAL_ASSESSMENT_CACHE:
            analysis = {**analysis, **GLOBAL_ASSESSMENT_CACHE["latest"]}

    elif analysis and isinstance(analysis, dict) and analysis.get("module") == "blood":
        from app.models.symptoms_analyzer import GLOBAL_ASSESSMENT_CACHE
        report_id = analysis.get("report_id")
        if report_id and report_id in GLOBAL_ASSESSMENT_CACHE:
            analysis = {**analysis, **GLOBAL_ASSESSMENT_CACHE[report_id]}
        elif "latest_blood" in GLOBAL_ASSESSMENT_CACHE:
            analysis = {**analysis, **GLOBAL_ASSESSMENT_CACHE["latest_blood"]}
        analysis.setdefault("biomarkers", [])
        analysis.setdefault("recommendations", [])

    elif analysis and isinstance(analysis, dict) and analysis.get("module") == "xray":
        from app.models.symptoms_analyzer import GLOBAL_ASSESSMENT_CACHE
        report_id = analysis.get("report_id")
        if report_id and report_id in GLOBAL_ASSESSMENT_CACHE:
            analysis = {**analysis, **GLOBAL_ASSESSMENT_CACHE[report_id]}
        elif "latest_xray" in GLOBAL_ASSESSMENT_CACHE:
            analysis = {**analysis, **GLOBAL_ASSESSMENT_CACHE["latest_xray"]}
        analysis.setdefault("top_predictions", [])
        analysis.setdefault("radiological_signs", [])
        analysis.setdefault("differential_diagnoses", [])

    elif not analysis and module == "symptoms":
        from app.models.symptoms_analyzer import GLOBAL_ASSESSMENT_CACHE
        if "latest" in GLOBAL_ASSESSMENT_CACHE:
            analysis = dict(GLOBAL_ASSESSMENT_CACHE["latest"])

    elif not analysis and module == "blood":
        from app.models.symptoms_analyzer import GLOBAL_ASSESSMENT_CACHE
        if "latest_blood" in GLOBAL_ASSESSMENT_CACHE:
            analysis = dict(GLOBAL_ASSESSMENT_CACHE["latest_blood"])

    elif not analysis and module == "xray":
        from app.models.symptoms_analyzer import GLOBAL_ASSESSMENT_CACHE
        if "latest_xray" in GLOBAL_ASSESSMENT_CACHE:
            analysis = dict(GLOBAL_ASSESSMENT_CACHE["latest_xray"])

    # Final safety defaults for symptoms so template never crashes
    if analysis and isinstance(analysis, dict) and analysis.get("module") == "symptoms":
        if "patient_profile" not in analysis or not isinstance(analysis.get("patient_profile"), dict):
            analysis["patient_profile"] = {
                "age": "Not Specified",
                "temperature": "Not Recorded",
                "allergies": [],
                "conditions": [],
                "current_medicines": "None Reported",
                "pregnancy_status": "Not Applicable"
            }
        else:
            # Ensure temperature is always a string
            pp = analysis["patient_profile"]
            if not isinstance(pp.get("temperature"), str):
                pp["temperature"] = str(pp.get("temperature", "Not Recorded"))
        analysis.setdefault("red_flags", [])
        analysis.setdefault("differentials", [])
        analysis.setdefault("medicine_cards", [])
        analysis.setdefault("is_emergency", False)
        analysis.setdefault("urgency_badge", "bg-primary text-white")
        analysis.setdefault("urgency_level", "MODERATE")
        analysis.setdefault("urgency_title", "CLINICAL EVALUATION RECOMMENDED")

    return render_template("dashboard/results.html", module=module, analysis=analysis)

@dashboard_bp.route("/history")
@login_required
def history():
    """Page 14: User history page (loads live user-specific records from MySQL)."""
    user_id = session.get("user_id")
    history_records = []
    
    try:
        with get_db() as cursor:
            cursor.execute(
                """SELECT id, module_type, summary_label, confidence_or_status, created_at 
                   FROM analysis_history 
                   WHERE user_id = %s 
                   ORDER BY created_at DESC""",
                (user_id,)
            )
            history_records = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching history from MySQL: {e}")

    return render_template("dashboard/history.html", records=history_records)

@dashboard_bp.route("/history/export")
@login_required
def export_history():
    """Exports user analysis history as downloadable CSV or JSON."""
    user_id = session.get("user_id")
    export_format = request.args.get("format", "csv").lower()

    try:
        with get_db() as cursor:
            cursor.execute(
                """SELECT id, module_type, summary_label, confidence_or_status, created_at 
                   FROM analysis_history 
                   WHERE user_id = %s 
                   ORDER BY created_at DESC""",
                (user_id,)
            )
            records = cursor.fetchall()
    except Exception as e:
        records = []

    if export_format == "json":
        from flask import jsonify
        return jsonify({
            "user_id": user_id,
            "exported_at": str(time.time()),
            "total_records": len(records),
            "records": records
        })
    else:
        # Default CSV export
        import io
        import csv
        from flask import Response

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Record ID", "Date & Time", "Domain Module", "Predicted Classification / Summary", "Confidence or Status"])

        for r in records:
            writer.writerow([
                r["id"],
                str(r["created_at"]),
                r["module_type"].capitalize(),
                r["summary_label"],
                r["confidence_or_status"]
            ])

        csv_data = output.getvalue()
        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment; filename=biohealth_analysis_history_{user_id}.csv"}
        )

@dashboard_bp.route("/history/clear", methods=["POST"])
@login_required
def clear_history():
    """Clears all analysis history for the logged-in user."""
    user_id = session.get("user_id")
    try:
        with get_db() as cursor:
            cursor.execute("DELETE FROM analysis_history WHERE user_id = %s", (user_id,))
            cursor.execute("DELETE FROM plant_detection_results WHERE user_id = %s", (user_id,))
            cursor.execute("DELETE FROM crop_detection_results WHERE user_id = %s", (user_id,))
            cursor.execute("DELETE FROM skin_screening_results WHERE user_id = %s", (user_id,))
            cursor.execute("DELETE FROM xray_results WHERE user_id = %s", (user_id,))
            cursor.execute("DELETE FROM blood_reports WHERE user_id = %s", (user_id,))
            cursor.execute("DELETE FROM symptom_assessments WHERE user_id = %s", (user_id,))
        flash("Your analysis history has been cleared.", "info")
    except Exception as e:
        flash(f"Error clearing history: {str(e)}", "danger")

    return redirect(url_for("dashboard.history"))

@dashboard_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Page 15: User profile page with update and account deletion support."""
    user_id = session.get("user_id")
    
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "update_profile":
            fullname = request.form.get("fullname", "").strip()
            email = request.form.get("email", "").strip().lower()
            if fullname and email:
                try:
                    UserModel.update_profile(user_id, fullname, email)
                    session["user_name"] = fullname
                    session["user_email"] = email
                    flash("Profile updated successfully!", "success")
                except Exception as e:
                    flash(f"Error updating profile: {str(e)}", "danger")
            else:
                flash("Name and email cannot be empty.", "warning")

        elif action == "change_password":
            current_pass = request.form.get("current_password", "")
            new_pass = request.form.get("new_password", "")
            confirm_pass = request.form.get("confirm_new_password", "")
            
            full_user = UserModel.get_by_email(session.get("user_email"))
            
            if not UserModel.verify_password(full_user["password_hash"], current_pass):
                flash("Current password incorrect.", "danger")
            elif len(new_pass) < 6:
                flash("New password must be at least 6 characters.", "warning")
            elif new_pass != confirm_pass:
                flash("New passwords do not match.", "warning")
            else:
                UserModel.update_password(user_id, new_pass)
                flash("Password changed successfully!", "success")

        elif action == "delete_account":
            try:
                UserModel.delete_account(user_id)
                session.clear()
                flash("Your account and all associated medical records have been permanently deleted.", "info")
                return redirect(url_for("main.index"))
            except Exception as e:
                flash(f"Could not delete account: {str(e)}", "danger")

    user_info = UserModel.get_by_id(user_id) or {
        "fullname": session.get("user_name", "User"),
        "email": session.get("user_email", "user@example.com"),
        "created_at": "Recent"
    }

    return render_template("dashboard/profile.html", user=user_info)
