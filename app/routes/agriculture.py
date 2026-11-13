import os
import time
from pathlib import Path
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from werkzeug.utils import secure_filename

from app.models.plant_classifier import PlantClassifier
from app.models.crop_classifier import CropClassifier
from app.models.db import get_db

agri_bp = Blueprint("agriculture", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@agri_bp.route("/plant", methods=["GET", "POST"])
def plant_detection():
    """
    Page 6: Plant Disease Detection (Module 1).
    Uploads leaf image, executes AI classification, stores record in MySQL,
    and displays prevention & care recommendations.
    """
    model_ready = PlantClassifier.is_model_available()

    if request.method == "POST":
        if not model_ready:
            flash(
                "Plant Disease Model is currently unavailable. Please run 'py train_plant_model.py' to train and save the model weights.",
                "warning"
            )
            return render_template("agriculture/plant.html", model_ready=model_ready)

        if "leaf_image" not in request.files:
            flash("No file part in the request.", "danger")
            return redirect(request.url)

        file = request.files["leaf_image"]
        if file.filename == "":
            flash("Please select a plant leaf image to analyze.", "warning")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Invalid file format. Please upload a JPG, JPEG, or PNG image.", "warning")
            return redirect(request.url)

        try:
            original_name = secure_filename(file.filename)
            unique_filename = f"plant_{int(time.time())}_{original_name}"
            
            upload_dir = Path(current_app.config["PLANT_UPLOAD_FOLDER"])
            upload_dir.mkdir(parents=True, exist_ok=True)
            save_path = upload_dir / unique_filename
            file.save(str(save_path))

            result = PlantClassifier.predict(str(save_path))

            if result["status"] != "success":
                flash(result.get("message", "Model analysis could not be completed."), "danger")
                return redirect(request.url)

            web_image_url = f"/static/uploads/plant/{unique_filename}"
            user_id = session.get("user_id")

            if user_id:
                try:
                    with get_db() as cursor:
                        cursor.execute(
                            """INSERT INTO plant_detection_results 
                               (user_id, image_path, predicted_class, confidence, disease_info, prevention_methods, is_healthy)
                               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                            (
                                user_id,
                                web_image_url,
                                result["display_name"],
                                result["confidence"],
                                f"{result['scientific_name']} - {result['symptoms']}",
                                f"{result['prevention']} Treatment: {result['treatment']}",
                                result["is_healthy"]
                            )
                        )
                        record_id = cursor.lastrowid

                        cursor.execute(
                            """INSERT INTO analysis_history (user_id, module_type, record_id, summary_label, confidence_or_status)
                               VALUES (%s, %s, %s, %s, %s)""",
                            (
                                user_id,
                                "plant",
                                record_id,
                                result["display_name"],
                                f"{result['confidence']}%"
                            )
                        )
                except Exception as db_err:
                    print(f"Notice: Could not save scan to MySQL database: {db_err}")

            session["last_analysis"] = {
                "module": "plant",
                "image_url": web_image_url,
                "title": result["display_name"],
                "subtitle": result["scientific_name"],
                "plant": result["plant"],
                "is_healthy": result["is_healthy"],
                "confidence": result["confidence"],
                "symptoms": result["symptoms"],
                "prevention": result["prevention"],
                "treatment": result["treatment"],
                "report_id": f"PLANT-{int(time.time())}"
            }

            flash(f"Analysis Complete: Identified {result['display_name']} with {result['confidence']}% confidence.", "success")
            return redirect(url_for("dashboard.results", module="plant"))

        except Exception as e:
            flash(f"An unexpected error occurred during image processing: {str(e)}", "danger")
            return redirect(request.url)

    return render_template("agriculture/plant.html", model_ready=model_ready)

@agri_bp.route("/crop", methods=["GET", "POST"])
def crop_detection():
    """
    Page 7: Crop Disease Detection (Module 2).
    Dedicated model for staple crops: Rice, Wheat, and Maize.
    Saves results into MySQL 'crop_detection_results' table.
    """
    model_ready = CropClassifier.is_model_available()

    if request.method == "POST":
        if not model_ready:
            flash(
                "Dedicated Crop Disease Model is currently unavailable. Please run 'py train_crop_model.py' first.",
                "warning"
            )
            return render_template("agriculture/crop.html", model_ready=model_ready)

        if "crop_image" not in request.files:
            flash("No file part in the request.", "danger")
            return redirect(request.url)

        file = request.files["crop_image"]
        if file.filename == "":
            flash("Please upload a crop photograph to analyze.", "warning")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Invalid format. Please upload a JPG, JPEG, or PNG image.", "warning")
            return redirect(request.url)

        crop_type = request.form.get("crop_type", "rice").lower()

        try:
            original_name = secure_filename(file.filename)
            unique_filename = f"crop_{int(time.time())}_{original_name}"
            
            upload_dir = Path(current_app.config["CROP_UPLOAD_FOLDER"])
            upload_dir.mkdir(parents=True, exist_ok=True)
            save_path = upload_dir / unique_filename
            file.save(str(save_path))

            # Run Dedicated Crop Inference
            result = CropClassifier.predict(str(save_path), target_crop=crop_type)

            if result["status"] != "success":
                flash(result.get("message", "Crop model analysis could not be completed."), "danger")
                return redirect(request.url)

            web_image_url = f"/static/uploads/crop/{unique_filename}"
            user_id = session.get("user_id")

            if user_id:
                try:
                    with get_db() as cursor:
                        cursor.execute(
                            """INSERT INTO crop_detection_results 
                               (user_id, crop_type, image_path, predicted_class, confidence, symptoms, prevention_info)
                               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                            (
                                user_id,
                                crop_type,
                                web_image_url,
                                result["display_name"],
                                result["confidence"],
                                f"{result['scientific_name']} - {result['symptoms']}",
                                f"{result['prevention']} Treatment: {result['treatment']}"
                            )
                        )
                        record_id = cursor.lastrowid

                        cursor.execute(
                            """INSERT INTO analysis_history (user_id, module_type, record_id, summary_label, confidence_or_status)
                               VALUES (%s, %s, %s, %s, %s)""",
                            (
                                user_id,
                                "crop",
                                record_id,
                                result["display_name"],
                                f"{result['confidence']}%"
                            )
                        )
                except Exception as db_err:
                    print(f"Notice: Could not save crop scan to MySQL: {db_err}")

            session["last_analysis"] = {
                "module": "crop",
                "image_url": web_image_url,
                "title": result["display_name"],
                "subtitle": result["scientific_name"],
                "plant": f"Staple Crop ({crop_type.capitalize()})",
                "is_healthy": result["is_healthy"],
                "confidence": result["confidence"],
                "symptoms": result["symptoms"],
                "prevention": result["prevention"],
                "treatment": result["treatment"],
                "report_id": f"CROP-{int(time.time())}"
            }

            flash(f"Crop Analysis Complete: Identified {result['display_name']} with {result['confidence']}% confidence.", "success")
            return redirect(url_for("dashboard.results", module="crop"))

        except Exception as e:
            flash(f"An unexpected error occurred during crop analysis: {str(e)}", "danger")
            return redirect(request.url)

    return render_template("agriculture/crop.html", model_ready=model_ready)
