"""
BioHealth AI - Programmatic REST API Gateway (Phase 12)
------------------------------------------------------
Enables programmatic integration for mobile apps, IoT edge scanners,
and external healthcare/agricultural software systems.
Base URL: /api/v1
"""

import os
import time
import uuid
from pathlib import Path
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

from app.models.plant_classifier import PlantClassifier
from app.models.crop_classifier import CropClassifier
from app.models.skin_classifier import SkinClassifier
from app.models.xray_classifier import XrayClassifier
from app.models.symptoms_analyzer import SymptomsAnalyzer
from app.models.pharmacopeia_data import VERIFIED_MEDICINES

api_bp = Blueprint("api", __name__)

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

@api_bp.route("/health", methods=["GET"])
def api_health():
    """System and AI model availability status API."""
    return jsonify({
        "status": "healthy",
        "api_version": "1.0.0",
        "system": "BioHealth AI Multi-Domain Diagnostic Engine",
        "active_models": {
            "plant_pathology": PlantClassifier.is_model_available(),
            "crop_screening": CropClassifier.is_model_available(),
            "skin_screening": SkinClassifier.is_model_available(),
            "xray_analysis": XrayClassifier.is_model_available(),
            "blood_ocr": True,
            "symptoms_triage": True
        },
        "timestamp": time.time()
    }), 200

@api_bp.route("/predict/plant", methods=["POST"])
def predict_plant():
    """Classifies plant leaf image and returns diagnosis and treatment plan."""
    if "image" not in request.files:
        return jsonify({"error": "No 'image' file provided in multipart/form-data."}), 400

    file = request.files["image"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format. Upload a PNG, JPG, or JPEG image."}), 400

    temp_dir = Path(current_app.config["PLANT_UPLOAD_FOLDER"])
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_path = temp_dir / f"api_plant_{uuid.uuid4().hex[:8]}.jpg"
    file.save(str(temp_path))

    try:
        prediction = PlantClassifier.predict(str(temp_path))
        return jsonify({
            "status": "success",
            "module": "plant_pathology",
            "prediction": prediction
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route("/predict/crop", methods=["POST"])
def predict_crop():
    """Classifies staple crop leaf image (Rice, Wheat, Maize)."""
    if "image" not in request.files:
        return jsonify({"error": "No 'image' file provided in multipart/form-data."}), 400

    file = request.files["image"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format. Upload a PNG, JPG, or JPEG image."}), 400

    temp_dir = Path(current_app.config["CROP_UPLOAD_FOLDER"])
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_path = temp_dir / f"api_crop_{uuid.uuid4().hex[:8]}.jpg"
    file.save(str(temp_path))

    try:
        prediction = CropClassifier.predict(str(temp_path))
        return jsonify({
            "status": "success",
            "module": "crop_protection",
            "prediction": prediction
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route("/predict/skin", methods=["POST"])
def predict_skin():
    """Evaluates skin lesion photograph across 7 HAM10000 categories."""
    if "image" not in request.files:
        return jsonify({"error": "No 'image' file provided in multipart/form-data."}), 400

    file = request.files["image"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format. Upload a PNG, JPG, or JPEG image."}), 400

    temp_dir = Path(current_app.config["SKIN_UPLOAD_FOLDER"])
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_path = temp_dir / f"api_skin_{uuid.uuid4().hex[:8]}.jpg"
    file.save(str(temp_path))

    try:
        prediction = SkinClassifier.predict(str(temp_path))
        return jsonify({
            "status": "success",
            "module": "dermatology_screening",
            "prediction": prediction,
            "disclaimer": "Experimental computer vision prototype. Non-diagnostic."
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route("/predict/xray", methods=["POST"])
def predict_xray():
    """Analyzes frontal thoracic radiograph (Chest X-Ray)."""
    if "image" not in request.files:
        return jsonify({"error": "No 'image' file provided in multipart/form-data."}), 400

    file = request.files["image"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format. Upload a PNG, JPG, or JPEG image."}), 400

    temp_dir = Path(current_app.config["XRAY_UPLOAD_FOLDER"])
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_path = temp_dir / f"api_xray_{uuid.uuid4().hex[:8]}.jpg"
    file.save(str(temp_path))

    try:
        prediction = XrayClassifier.predict(str(temp_path))
        return jsonify({
            "status": "success",
            "module": "thoracic_radiography",
            "prediction": prediction,
            "disclaimer": "Investigational research model. Mandatory review by a licensed radiologist required."
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route("/triage/symptoms", methods=["POST"])
def triage_symptoms():
    """Evaluates reported symptoms, vitals, and contraindications."""
    data = request.get_json(silent=True) or {}
    symptoms = data.get("symptoms", [])

    if not symptoms:
        return jsonify({"error": "Request body must include 'symptoms' array."}), 400

    try:
        analysis = SymptomsAnalyzer.evaluate(
            selected_symptoms=symptoms,
            duration=data.get("duration", "days"),
            severity=data.get("severity", "moderate"),
            age=data.get("age"),
            temperature_val=data.get("temperature"),
            temperature_unit=data.get("temperature_unit", "F"),
            allergies=data.get("allergies", []),
            conditions=data.get("conditions", []),
            current_medicines=data.get("current_medicines", ""),
            pregnancy_status=data.get("pregnancy_status", "none"),
            additional_notes=data.get("notes", "")
        )
        return jsonify({
            "status": "success",
            "module": "symptoms_triage",
            "triage_result": analysis
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route("/medicines", methods=["GET"])
def search_medicines():
    """Queries verified pharmacopeia knowledge base."""
    query = request.args.get("query", "").strip().lower()

    if query:
        matches = [
            m for m in VERIFIED_MEDICINES
            if (
                query in m["name"].lower()
                or query in m["generic_name"].lower()
                or query in m.get("brand_examples", "").lower()
                or query in m["category"].lower()
                or query in m["uses"].lower()
            )
        ]
    else:
        matches = VERIFIED_MEDICINES

    return jsonify({
        "status": "success",
        "total_results": len(matches),
        "query": query,
        "medicines": matches
    }), 200

