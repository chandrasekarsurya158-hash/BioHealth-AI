# BioHealth AI: Multi-Domain AI Disease Detection & Intelligent Health Assistance System

[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Flask 3.0](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![MySQL XAMPP](https://img.shields.io/badge/Database-MySQL%20(InnoDB)-orange.svg)](https://www.apachefriends.org/)
[![Bootstrap 5](https://img.shields.io/badge/Frontend-Bootstrap%205-purple.svg)](https://getbootstrap.com/)
[![Automated Tests](https://img.shields.io/badge/Tests-15%20Passed-success.svg)](test_system.py)

---

## 1. Executive Summary

**BioHealth AI** is a production-grade, multi-domain web platform uniting computer vision, natural language biomarker extraction, and clinical rule-based triage engines into one unified interface. The system bridges two critical societal challenges:
1. **Agricultural Security:** Early visual detection of pathogen attacks on crop leaves and staple grains (Rice, Wheat, Maize) to safeguard food yields.
2. **Clinical Health Assistance:** Non-diagnostic clinical triage, laboratory blood report analysis, frontal chest radiograph evaluation, and pharmacopeia safety checks.

---

## 2. Technical Stack & Architecture

* **Web Framework:** Flask 3.0 with modular Blueprints (`main`, `auth`, `agriculture`, `medical`, `dashboard`, `admin`)
* **Database Engine:** MySQL 8 / MariaDB (XAMPP) via pure-Python `PyMySQL` with connection pooling and parameterization
* **Document Intelligence & OCR:** `PyMuPDF` (`fitz`) for PDF text layer extraction, bounding boxes, and regex biomarker normalization
* **Machine Learning / Computer Vision:** `NumPy`, `Pillow`, `OpenCV`, `Scikit-Learn` feature projectors and neural classifier inference engines
* **Frontend UI:** Bootstrap 5.3.3, Bootstrap Icons 1.11, Google Fonts (*Plus Jakarta Sans*), Chart.js data visualizations
* **Report Generation:** Native `@media print` optimized paper/PDF report stylesheets and downloadable CSV / JSON data streams

---

## 3. Core Functional Modules

| Module ID | Domain & Focus | AI / Technical Methodology | Target Classes / Indicators |
|---|---|---|---|
| **Module 1** | **Plant Leaf Disease** | MobileNetV2 / Heuristic CNN | Apple Scab, Black Rot, Cedar Rust, Healthy Foliage |
| **Module 2** | **Staple Crops (Rice, Wheat, Maize)** | ResNet50 / Multiclass Engine | Rice Blast, Brown Spot, Wheat Rust, Maize Blight |
| **Module 3 / 4D** | **Dermatology Screening** | EfficientNet-B0 (HAM10000) | Melanocytic Nevi, Melanoma, Basal Cell Carcinoma, Actinic Keratosis, Vascular |
| **Module 4A** | **Symptoms Health Triage** | Evidence-Based Rule Engine | Acute Triage, Red-Flag Detection, Allergy & Pregnancy Contraindication |
| **Module 4B** | **Blood Biomarkers & OCR** | PyMuPDF + Regex Normalizer | 12 Essential Biomarkers (Hb, FBG, HbA1c, WBC, RBC, Platelets, Creatinine, etc.) |
| **Module 4C** | **Thoracic Radiography (X-Ray)** | DenseNet-121 Feature Engine | Normal Thoracic Cavity, Bacterial Pneumonia, Viral Pneumonia, Tuberculosis |
| **Module 4E** | **Verified Pharmacopeia** | WHO & BNF Reference Database | Uses, Precautions, Black Box Warnings, Contraindications, Drug Interactions |

---

## 4. Application Map & URL Endpoints

* **Public Portals:**
  * Landing Page: `GET /`
  * Emergency Helplines & Specialist Directory: `GET /emergency-directory`
  * System Health Check: `GET /health-check`
* **Authentication:**
  * User Registration: `GET /auth/register` \| `POST /auth/register`
  * User Sign In: `GET /auth/login` \| `POST /auth/login`
  * Sign Out: `GET /auth/logout`
* **Agricultural AI:**
  * Plant Leaf Detection: `GET /agriculture/plant` \| `POST /agriculture/plant`
  * Crop Health Screening: `GET /agriculture/crop` \| `POST /agriculture/crop`
* **Medical Health AI:**
  * Skin Lesion Screening: `GET /medical/skin` \| `POST /medical/skin`
  * Symptoms Triage: `GET /medical/symptoms` \| `POST /medical/symptoms`
  * Blood Report OCR: `GET /medical/blood-report` \| `POST /medical/blood-report`
  * Chest X-Ray Screening: `GET /medical/xray` \| `POST /medical/xray`
  * Pharmacopeia Reference: `GET /medical/medicine` (Supports `?query=...`)
* **User Dashboard & Analytics:**
  * User Dashboard: `GET /dashboard/` (With live MySQL Chart.js activity monitor)
  * Multi-Domain Results: `GET /dashboard/results?module={plant|crop|skin|blood|xray|symptoms}`
  * Scan History: `GET /dashboard/history`
  * History Data Export: `GET /dashboard/history/export?format={csv|json}`
  * History Purge: `POST /dashboard/history/clear`
  * User Profile & Security: `GET /dashboard/profile` \| `POST /dashboard/profile`
* **Administrator Console:**
  * Admin Sign In: `GET /admin/login` \| `POST /admin/login`
  * Admin Analytics: `GET /admin/dashboard`
  * Admin Sign Out: `GET /admin/logout`

---

## 5. Database Schema (MySQL `multi_disease_db`)

The database utilizes InnoDB with foreign keys and cascade rules across 12 normalized tables:
1. `users`: Authentication records, email indexing, password hashes (PBKDF2:SHA256)
2. `admins`: Administrative accounts and privileges
3. `analysis_history`: Centralized user scan timeline across all 6 modules
4. `plant_detection_results`: Plant leaf scan metadata and predictions
5. `crop_detection_results`: Crop leaf scan metadata and treatment plans
6. `skin_screening_results`: Dermatological screening risk scores and consents
7. `symptom_assessments`: Structured triage assessments, red-flags, and JSON symptoms
8. `blood_reports`: Uploaded laboratory PDF metadata and summary statements
9. `blood_test_values`: Normalized 1:N individual biomarkers extracted from reports
10. `xray_results`: Thoracic radiography classification and radiologist disclaimers
11. `medicines`: Verified pharmacopeia knowledge base
12. `medicine_references`: Clinical citations and journal sources

---

## 6. Installation & Quick Start

### Prerequisites
* Python 3.9 – 3.13
* XAMPP with Apache and MySQL running (Port 3306)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Initialize Database & Seed Admins
```bash
py init_db.py
```
*Creates all 12 tables and seeds default administrator: `admin` / `admin123`.*

### Step 3: Verify Setup
```bash
py verify_setup.py
```

### Step 4: Run Application
```bash
py run.py
```
*Access local web application at: [http://127.0.0.1:5000](http://127.0.0.1:5000)*

---

## 7. Running the Automated Test Suite

BioHealth AI includes a complete automated unit and integration test suite:
```bash
py test_system.py
```

**Test Coverage Summary:**
* `test_01_database_connectivity`: Validates MySQL schema and table presence.
* `test_02_public_http_routes`: Tests HTTP 200 responses on all 13 public routes.
* `test_03_symptoms_triage_emergency_detection`: Verifies hyperpyrexia ($108^\circ\text{F}$) triage alert rules.
* `test_04_blood_report_biomarker_extraction`: Tests PyMuPDF OCR extraction on lab reports.
* `test_05_xray_model_inference`: Validates DenseNet-121 thoracic radiograph classifier.
* `test_06_pharmacopeia_medicine_search`: Validates drug precaution and indication indexing.
* `test_07_auth_redirection`: Verifies session enforcement on private endpoints.
* `test_08_history_export_formats`: Tests downloadable CSV and JSON data export streams.

---

## 8. Clinical & Ethical Disclaimers

> **IMPORTANT MEDICAL NOTICE:** All medical detection tools (Skin Screening, Blood Report OCR, Chest X-Ray Analysis, Symptoms Triage, and Medicine Precautions) are experimental computational research aids and do **NOT** provide a confirmed medical diagnosis. They must never replace professional evaluation by a licensed physician or radiologist.
>
> In the event of acute chest pain, severe shortness of breath, uncontrolled hemorrhage, or severe injury, contact national emergency medical services (112 / 911 / 999) immediately.
