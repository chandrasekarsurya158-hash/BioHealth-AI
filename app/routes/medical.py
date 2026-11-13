import os
import json
import time
import uuid
from pathlib import Path
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from werkzeug.utils import secure_filename

from app.models.skin_classifier import SkinClassifier
from app.models.symptoms_analyzer import SymptomsAnalyzer
from app.models.symptoms_data import (
    SUPPORTED_SYMPTOMS,
    SUPPORTED_CONDITIONS,
    SUPPORTED_ALLERGIES
)
from app.models.db import get_db

medical_bp = Blueprint("medical", __name__)

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_image(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

@medical_bp.route("/skin", methods=["GET", "POST"])
def skin_screening():
    """
    Page 8: Skin Disease Screening (Module 3 / 4D).
    Evaluates skin lesion photograph across 7 HAM10000 benchmark categories.
    """
    model_ready = SkinClassifier.is_model_available()

    if request.method == "POST":
        if not model_ready:
            flash("Dermatological Screening Model is currently unavailable. Please run 'py train_skin_model.py' first.", "warning")
            return render_template("medical/skin.html", model_ready=model_ready)

        if "skin_image" not in request.files:
            flash("No file uploaded in the request.", "danger")
            return redirect(request.url)

        file = request.files["skin_image"]
        if file.filename == "":
            flash("Please upload a clear skin photograph.", "warning")
            return redirect(request.url)

        if not allowed_image(file.filename):
            flash("Invalid file format. Please upload a JPG, JPEG, or PNG image.", "warning")
            return redirect(request.url)

        consent_agreed = request.form.get("consent_agreed")
        if not consent_agreed:
            flash("You must acknowledge that this tool is experimental and does not provide a confirmed medical diagnosis.", "warning")
            return redirect(request.url)

        try:
            original_name = secure_filename(file.filename)
            unique_filename = f"skin_{int(time.time())}_{original_name}"

            upload_dir = Path(current_app.config["SKIN_UPLOAD_FOLDER"])
            upload_dir.mkdir(parents=True, exist_ok=True)
            save_path = upload_dir / unique_filename
            file.save(str(save_path))

            result = SkinClassifier.predict(str(save_path))

            if result["status"] != "success":
                flash(result.get("message", "Skin screening could not be completed."), "danger")
                return redirect(request.url)

            web_image_url = f"/static/uploads/skin/{unique_filename}"
            user_id = session.get("user_id")

            if user_id:
                try:
                    with get_db() as cursor:
                        cursor.execute(
                            """INSERT INTO skin_screening_results 
                               (user_id, image_path, predicted_category, confidence, risk_notes, disclaimer_agreed)
                               VALUES (%s, %s, %s, %s, %s, %s)""",
                            (
                                user_id,
                                web_image_url,
                                result["display_name"],
                                result["confidence"],
                                f"{result['urgency']} - {result['recommendation']}",
                                True
                            )
                        )
                        record_id = cursor.lastrowid

                        cursor.execute(
                            """INSERT INTO analysis_history (user_id, module_type, record_id, summary_label, confidence_or_status)
                               VALUES (%s, %s, %s, %s, %s)""",
                            (
                                user_id,
                                "skin",
                                record_id,
                                result["display_name"],
                                f"{result['confidence']}%"
                            )
                        )
                except Exception as db_err:
                    print(f"Notice: Could not save skin screening to MySQL: {db_err}")

            session["last_analysis"] = {
                "module": "skin",
                "image_url": web_image_url,
                "title": result["display_name"],
                "subtitle": result["category_type"],
                "plant": "Cutaneous Dermatological Screening (HAM10000)",
                "is_healthy": result["is_benign"],
                "confidence": result["confidence"],
                "urgency": result["urgency"],
                "urgency_badge": result["urgency_badge"],
                "symptoms": result["description"],
                "prevention": result["abcde_assessment"],
                "treatment": result["recommendation"],
                "risk_notes": result["risk_notes"],
                "report_id": f"DERM-{int(time.time())}"
            }

            flash(f"Screening Complete: Categorized as '{result['display_name']}' ({result['confidence']}% confidence).", "info")
            return redirect(url_for("dashboard.results", module="skin"))

        except Exception as e:
            flash(f"An unexpected error occurred during skin image processing: {str(e)}", "danger")
            return redirect(request.url)

    return render_template("medical/skin.html", model_ready=model_ready)

@medical_bp.route("/symptoms", methods=["GET", "POST"])
def symptoms_assessment():
    """
    Page 9: Symptoms-Based Health Assessment (Module 4A - Upgraded Triage).
    Collects patient background, evaluates dangerous temperatures & red flags FIRST,
    matches against reviewed syndromic knowledge base, cross-checks medication
    contraindications against patient allergies/conditions, and stores records in MySQL.
    """
    if request.method == "POST":
        selected_symptoms = request.form.getlist("symptoms")
        duration = request.form.get("duration", "less_24h")
        severity = request.form.get("severity", "mild").lower()
        age = request.form.get("age", "").strip()
        temperature_val = request.form.get("temperature", "").strip()
        temperature_unit = request.form.get("temp_unit", "F").strip()
        allergies = request.form.getlist("allergies")
        conditions = request.form.getlist("conditions")
        current_medicines = request.form.get("current_medicines", "").strip()
        pregnancy_status = request.form.get("pregnancy", "none")
        notes = request.form.get("notes", "").strip()

        if not selected_symptoms:
            flash("Please select at least one symptom to evaluate.", "warning")
            return redirect(url_for("medical.symptoms_assessment"))

        # Run Upgraded Clinical Triage Evaluation
        result = SymptomsAnalyzer.evaluate(
            selected_symptoms=selected_symptoms,
            duration=duration,
            severity=severity,
            age=age,
            temperature_val=temperature_val,
            temperature_unit=temperature_unit,
            allergies=allergies,
            conditions=conditions,
            current_medicines=current_medicines,
            pregnancy_status=pregnancy_status,
            additional_notes=notes
        )

        user_id = session.get("user_id")

        # Save to MySQL if logged in
        if user_id:
            try:
                flags_text = " | ".join([f["reason"] for f in result["red_flags"]]) if result["red_flags"] else "None"
                # Store full patient metadata in additional_notes for backward compatibility
                patient_meta_summary = json.dumps({
                    "age": result["patient_profile"]["age"],
                    "temperature": result["patient_profile"]["temperature"],
                    "allergies": result["patient_profile"]["allergies"],
                    "conditions": result["patient_profile"]["conditions"],
                    "current_medicines": result["patient_profile"]["current_medicines"],
                    "pregnancy": result["patient_profile"]["pregnancy_status"],
                    "user_notes": notes
                })

                with get_db() as cursor:
                    cursor.execute(
                        """INSERT INTO symptom_assessments 
                           (user_id, symptoms_json, duration, severity, additional_notes, possible_explanations, urgency_level, warning_flags)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (
                            user_id,
                            json.dumps(selected_symptoms),
                            duration,
                            severity,
                            patient_meta_summary,
                            result["primary_syndrome"] + ": " + result["primary_explanation"],
                            result["urgency_level"].lower(),
                            flags_text
                        )
                    )
                    record_id = cursor.lastrowid

                    cursor.execute(
                        """INSERT INTO analysis_history (user_id, module_type, record_id, summary_label, confidence_or_status)
                           VALUES (%s, %s, %s, %s, %s)""",
                        (
                            user_id,
                            "symptoms",
                            record_id,
                            result["primary_syndrome"],
                            f"Urgency: {result['urgency_level']}"
                        )
                    )
            except Exception as db_err:
                print(f"Notice: Could not save symptoms assessment to MySQL: {db_err}")

        # Store in server-side cache to bypass 4KB cookie limits
        from app.models.symptoms_analyzer import GLOBAL_ASSESSMENT_CACHE
        report_id = f"SYM-{int(time.time())}"
        
        full_analysis_data = {
            "module": "symptoms",
            "report_id": report_id,
            "title": result["primary_syndrome"],
            "subtitle": f"Triage Priority: {result['urgency_title']}",
            "plant": "Clinical Health Assistant (Module 4A)",
            "is_emergency": result["is_emergency"],
            "urgency_level": result["urgency_level"],
            "urgency_badge": result["urgency_badge"],
            "urgency_title": result["urgency_title"],
            "red_flags": result["red_flags"],
            "patient_profile": result["patient_profile"],
            "selected_symptoms": result["selected_symptoms"],
            "duration": result["duration"],
            "severity": result["severity"],
            "notes": result["notes"],
            "matching_rationale": result["matching_rationale"],
            "explanation": result["primary_explanation"],
            "differentials": result["differentials"],
            "guidance": result["home_guidance"],
            "when_to_seek_care": result["when_to_seek_care"],
            "medicine_cards": result["medicine_cards"]
        }
        
        GLOBAL_ASSESSMENT_CACHE[report_id] = full_analysis_data
        GLOBAL_ASSESSMENT_CACHE["latest"] = full_analysis_data

        # Save to MySQL (symptom_assessments & analysis_history)
        user_id = session.get("user_id")
        try:
            with get_db() as cursor:
                urgency_val = str(result.get("urgency_level", "moderate")).lower()
                if urgency_val not in ("low", "moderate", "high", "emergency"):
                    urgency_val = "emergency" if result.get("is_emergency") else "moderate"

                sev_val = str(result.get("severity", "moderate")).lower()
                if sev_val not in ("mild", "moderate", "severe"):
                    sev_val = "moderate"

                cursor.execute(
                    """INSERT INTO symptom_assessments 
                       (user_id, symptoms_json, duration, severity, additional_notes, possible_explanations, urgency_level, warning_flags)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (
                        user_id,
                        json.dumps(result.get("selected_symptoms", [])),
                        str(result.get("duration", "Recent")),
                        sev_val,
                        str(result.get("notes", "")),
                        str(result.get("primary_explanation", "")),
                        urgency_val,
                        json.dumps([rf.get("title", "") for rf in result.get("red_flags", [])])
                    )
                )
                db_symptom_id = cursor.lastrowid

                if user_id:
                    cursor.execute(
                        """INSERT INTO analysis_history (user_id, module_type, record_id, summary_label, confidence_or_status)
                           VALUES (%s, %s, %s, %s, %s)""",
                        (
                            user_id,
                            "symptoms",
                            db_symptom_id,
                            result["primary_syndrome"],
                            f"Triage: {result['urgency_level'].upper()}"
                        )
                    )
        except Exception as db_err:
            print(f"Notice: Could not save symptom assessment to MySQL: {db_err}")

        # Store compact pointer in browser session cookie (under 800 bytes)
        session["last_analysis"] = {
            "module": "symptoms",
            "report_id": report_id,
            "title": result["primary_syndrome"],
            "subtitle": f"Triage Priority: {result['urgency_title']}",
            "plant": "Clinical Health Assistant (Module 4A)",
            "is_emergency": result["is_emergency"],
            "urgency_level": result["urgency_level"],
            "urgency_badge": result["urgency_badge"],
            "patient_profile": result["patient_profile"],
            "duration": result["duration"],
            "severity": result["severity"]
        }
        session.modified = True

        if result["is_emergency"]:
            flash("EMERGENCY MEDICAL WARNING: High-risk symptoms or dangerous temperature detected. Immediate medical intervention required.", "danger")
        else:
            flash(f"Health Assessment Complete: Matched '{result['primary_syndrome']}'.", "success")

        return redirect(url_for("dashboard.results", module="symptoms"))

    return render_template(
        "medical/symptoms.html", 
        symptoms_dict=SUPPORTED_SYMPTOMS,
        conditions_dict=SUPPORTED_CONDITIONS,
        allergies_dict=SUPPORTED_ALLERGIES
    )

@medical_bp.route("/blood-report", methods=["GET", "POST"])
def blood_report():
    """
    Page 10: Blood report analysis (Module 4B, Phase 8).
    Extracts text using PyMuPDF (fitz) from uploaded lab PDF or image,
    identifies standard biomarkers, evaluates physiological ranges,
    stores records in MySQL, and presents structured clinical reports.
    """
    if request.method == "POST":
        if "report_file" not in request.files or request.files["report_file"].filename == "":
            flash("Please upload a PDF document or lab report image.", "warning")
            return redirect(url_for("medical.blood_report"))

        file = request.files["report_file"]
        orig_filename = secure_filename(file.filename)
        file_ext = os.path.splitext(orig_filename)[1].lower()

        allowed_extensions = {".pdf", ".png", ".jpg", ".jpeg"}
        if file_ext not in allowed_extensions:
            flash("Invalid file format. Please upload a PDF document or image file (.pdf, .png, .jpg).", "danger")
            return redirect(url_for("medical.blood_report"))

        # Generate unique filename and save file
        unique_name = f"blood_{uuid.uuid4().hex[:10]}_{int(time.time())}{file_ext}"
        upload_folder = os.path.join(current_app.root_path, "static", "uploads", "blood_reports")
        os.makedirs(upload_folder, exist_ok=True)
        save_path = os.path.join(upload_folder, unique_name)
        file.save(save_path)

        # Execute Document Extraction and Biomarker Parsing
        from app.models.blood_report_parser import BloodReportParser
        from app.models.symptoms_analyzer import GLOBAL_ASSESSMENT_CACHE

        raw_text = BloodReportParser.extract_text_from_file(save_path)
        parsed_result = BloodReportParser.parse_report_text(raw_text)

        report_id = f"BLD-{int(time.time())}"

        full_analysis_data = {
            "module": "blood",
            "report_id": report_id,
            "title": "Laboratory Blood Biomarker Assessment",
            "subtitle": f"Status: {parsed_result['overall_status']}",
            "plant": "Diagnostic Hematology & Biochemistry (Module 4B)",
            "overall_status": parsed_result["overall_status"],
            "overall_badge": parsed_result["overall_badge"],
            "urgency": parsed_result["urgency"],
            "summary_statement": parsed_result["summary_statement"],
            "total_extracted": parsed_result["total_extracted"],
            "normal_count": parsed_result["normal_count"],
            "abnormal_count": parsed_result["abnormal_count"],
            "critical_count": parsed_result["critical_count"],
            "recommendations": parsed_result["recommendations"],
            "biomarkers": parsed_result["biomarkers"],
            "raw_text_preview": parsed_result["raw_text_preview"],
            "disclaimer": parsed_result["disclaimer"],
            "file_name": orig_filename,
            "file_url": url_for("static", filename=f"uploads/blood_reports/{unique_name}")
        }

        # Cache rich dataset in server memory
        GLOBAL_ASSESSMENT_CACHE[report_id] = full_analysis_data
        GLOBAL_ASSESSMENT_CACHE["latest_blood"] = full_analysis_data
        GLOBAL_ASSESSMENT_CACHE["latest"] = full_analysis_data

        # Store compact pointer in browser session cookie (< 800 bytes)
        session["last_analysis"] = {
            "module": "blood",
            "report_id": report_id,
            "title": "Laboratory Blood Biomarker Assessment",
            "subtitle": f"Status: {parsed_result['overall_status']}",
            "plant": "Diagnostic Hematology & Biochemistry (Module 4B)",
            "overall_status": parsed_result["overall_status"],
            "overall_badge": parsed_result["overall_badge"],
            "urgency": parsed_result["urgency"],
            "total_extracted": parsed_result["total_extracted"],
            "abnormal_count": parsed_result["abnormal_count"]
        }
        session.modified = True

        # Save to MySQL (blood_reports & blood_test_values)
        user_id = session.get("user_id")
        try:
            with get_db() as cursor:
                cursor.execute(
                    """INSERT INTO blood_reports (user_id, file_path, file_type, extracted_text, overall_summary, disclaimer)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (
                        user_id,
                        f"uploads/blood_reports/{unique_name}",
                        file_ext.replace(".", ""),
                        parsed_result.get("raw_text_preview", ""),
                        parsed_result.get("summary_statement", ""),
                        parsed_result.get("disclaimer", "")
                    )
                )
                db_report_id = cursor.lastrowid

                # Save individual normalized biomarker rows
                for bio in parsed_result.get("biomarkers", []):
                    flag_val = bio["status"]
                    if "CRITICAL" in flag_val:
                        flag_val = "HIGH" if "HIGH" in flag_val else "LOW"
                    elif flag_val not in ("NORMAL", "HIGH", "LOW", "INDETERMINATE"):
                        flag_val = "INDETERMINATE"

                    cursor.execute(
                        """INSERT INTO blood_test_values 
                           (report_id, test_name, measured_value, unit, reference_range, flag, clinical_meaning)
                           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                        (
                            db_report_id,
                            bio["name"],
                            str(bio["measured_value"]),
                            bio["unit"],
                            bio["ref_range"],
                            flag_val,
                            bio["interpretation"]
                        )
                    )

                if user_id:
                    cursor.execute(
                        """INSERT INTO analysis_history (user_id, module_type, record_id, summary_label, confidence_or_status)
                           VALUES (%s, %s, %s, %s, %s)""",
                        (
                            user_id,
                            "blood",
                            db_report_id,
                            f"{parsed_result['total_extracted']} Biomarkers Extracted",
                            f"{parsed_result['abnormal_count']} Out-of-Range"
                        )
                    )
        except Exception as db_err:
            print(f"Notice: Could not save blood report to MySQL: {db_err}")

        if parsed_result["critical_count"] > 0:
            flash(f"Laboratory Analysis Complete: {parsed_result['critical_count']} critical outlier parameters detected! Immediate physician review recommended.", "danger")
        elif parsed_result["abnormal_count"] > 0:
            flash(f"Laboratory Analysis Complete: Extracted {parsed_result['total_extracted']} biomarkers ({parsed_result['abnormal_count']} out of range).", "warning")
        else:
            flash(f"Laboratory Analysis Complete: Extracted {parsed_result['total_extracted']} biomarkers (All within normal reference ranges).", "success")

        return redirect(url_for("dashboard.results", module="blood"))

    return render_template("medical/blood_report.html")

@medical_bp.route("/xray", methods=["GET", "POST"])
def xray_analysis():
    """
    Page 11: Chest X-ray analysis (Module 4C, Phase 9).
    Loads CheXNet DenseNet-121 model, classifies frontal thoracic radiographs,
    stores predictions in MySQL, and displays radiologist-level differential reports.
    """
    from app.models.xray_classifier import XrayClassifier
    model_ready = XrayClassifier.is_model_available()

    if request.method == "POST":
        if "xray_image" not in request.files or request.files["xray_image"].filename == "":
            flash("Please upload a frontal digital chest X-ray radiograph.", "warning")
            return redirect(url_for("medical.xray_analysis"))

        file = request.files["xray_image"]
        orig_filename = secure_filename(file.filename)

        if not allowed_image(orig_filename):
            flash("Invalid image format. Please upload a standard image radiograph (.jpg, .jpeg, .png).", "danger")
            return redirect(url_for("medical.xray_analysis"))

        unique_name = f"xray_{uuid.uuid4().hex[:10]}_{int(time.time())}.jpg"
        upload_folder = os.path.join(current_app.root_path, "static", "uploads", "xray")
        os.makedirs(upload_folder, exist_ok=True)
        save_path = os.path.join(upload_folder, unique_name)
        file.save(save_path)

        # Run Thoracic Feature Inference
        result = XrayClassifier.predict(save_path)

        report_id = f"XRAY-{int(time.time())}"
        user_id = session.get("user_id")

        # Save to MySQL
        try:
            with get_db() as cursor:
                cursor.execute(
                    """INSERT INTO xray_results 
                       (user_id, image_path, predicted_category, confidence, radiologist_disclaimer)
                       VALUES (%s, %s, %s, %s, %s)""",
                    (
                        user_id,
                        f"uploads/xray/{unique_name}",
                        result["display_name"],
                        result["confidence"],
                        result["radiologist_disclaimer"]
                    )
                )
                db_record_id = cursor.lastrowid

                if user_id:
                    cursor.execute(
                        """INSERT INTO analysis_history (user_id, module_type, record_id, summary_label, confidence_or_status)
                           VALUES (%s, %s, %s, %s, %s)""",
                        (
                            user_id,
                            "xray",
                            db_record_id,
                            result["display_name"],
                            f"{result['confidence']}% Confidence"
                        )
                    )
        except Exception as db_err:
            print(f"Notice: Could not save X-ray prediction to MySQL: {db_err}")

        # Store in server-side cache
        from app.models.symptoms_analyzer import GLOBAL_ASSESSMENT_CACHE

        full_analysis_data = {
            "module": "xray",
            "report_id": report_id,
            "title": result["display_name"],
            "subtitle": result["category_type"],
            "plant": "Thoracic Radiography & Pulmonary Screening (Module 4C)",
            "confidence": result["confidence"],
            "is_healthy": not result["is_abnormal"],
            "is_abnormal": result["is_abnormal"],
            "urgency": result["urgency"],
            "urgency_badge": result["urgency_badge"],
            "description": result["description"],
            "radiological_signs": result["radiological_signs"],
            "differential_diagnoses": result["differential_diagnoses"],
            "clinical_recommendation": result["clinical_recommendation"],
            "radiologist_disclaimer": result["radiologist_disclaimer"],
            "top_predictions": result["top_predictions"],
            "model_architecture": result["model_architecture"],
            "image_url": url_for("static", filename=f"uploads/xray/{unique_name}"),
            "file_name": orig_filename
        }

        GLOBAL_ASSESSMENT_CACHE[report_id] = full_analysis_data
        GLOBAL_ASSESSMENT_CACHE["latest_xray"] = full_analysis_data
        GLOBAL_ASSESSMENT_CACHE["latest"] = full_analysis_data

        # Store compact pointer in browser session cookie
        session["last_analysis"] = {
            "module": "xray",
            "report_id": report_id,
            "title": result["display_name"],
            "subtitle": result["category_type"],
            "plant": "Thoracic Radiography & Pulmonary Screening (Module 4C)",
            "confidence": result["confidence"],
            "is_healthy": not result["is_abnormal"],
            "is_abnormal": result["is_abnormal"],
            "urgency": result["urgency"],
            "urgency_badge": result["urgency_badge"],
            "image_url": url_for("static", filename=f"uploads/xray/{unique_name}")
        }
        session.modified = True

        if result["is_abnormal"]:
            flash(f"Radiography Screening Complete: Radiologic findings consistent with '{result['display_name']}' ({result['confidence']}% confidence).", "warning")
        else:
            flash(f"Radiography Screening Complete: Clear lung fields identified ({result['confidence']}% confidence).", "success")

        return redirect(url_for("dashboard.results", module="xray"))

    return render_template("medical/xray.html", model_ready=model_ready)

@medical_bp.route("/medicine", methods=["GET", "POST"])
def medicine_info():
    """
    Page 12: Medicine information (Module 4E, Phase 10).
    Searches verified pharmacopeia knowledge base for therapeutic uses,
    critical precautions, warnings, side effects, contraindications, and citations.
    """
    search_query = request.args.get("query", "").strip()
    from app.models.pharmacopeia_data import VERIFIED_MEDICINES

    if search_query:
        q_lower = search_query.lower()
        matched_medicines = [
            m for m in VERIFIED_MEDICINES
            if (
                q_lower in m["name"].lower()
                or q_lower in m["generic_name"].lower()
                or q_lower in m.get("brand_examples", "").lower()
                or q_lower in m["category"].lower()
                or q_lower in m["uses"].lower()
            )
        ]
    else:
        # Default view: show all verified medicines
        matched_medicines = VERIFIED_MEDICINES

    return render_template(
        "medical/medicine.html",
        query=search_query,
        medicines=matched_medicines,
        total_results=len(matched_medicines)
    )
