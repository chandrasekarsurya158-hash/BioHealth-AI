"""
Setup Verification Script for Multi-Domain AI Disease Detection System.
Run this script to verify:
1. Python version compatibility
2. Required Python libraries installation
3. Directory layout and write permissions
4. Optional MySQL (XAMPP) service availability
"""

import sys
import os
from pathlib import Path

def print_header(title):
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def check_python():
    print_header("1. Checking Python Environment")
    ver = sys.version_info
    print(f" Python Version Detected: {ver.major}.{ver.minor}.{ver.micro}")
    print(f" Executable Path: {sys.executable}")
    if ver.major == 3 and ver.minor >= 9:
        print(" [OK] Python version is compatible (>= 3.9).")
        return True
    else:
        print(" [WARNING] Python 3.9 or higher is strongly recommended.")
        return False

def check_packages():
    print_header("2. Checking Core Python Packages")
    required = {
        "flask": "Flask",
        "werkzeug": "Werkzeug",
        "dotenv": "python-dotenv",
        "pymysql": "PyMySQL",
        "cryptography": "cryptography",
        "PIL": "Pillow",
        "fitz": "PyMuPDF",
        "numpy": "numpy",
        "pandas": "pandas",
        "cv2": "opencv-python",
        "sklearn": "scikit-learn"
    }

    all_passed = True
    for module_name, pip_name in required.items():
        try:
            __import__(module_name)
            print(f" [INSTALLED] {pip_name}")
        except ImportError:
            print(f" [MISSING]   {pip_name} (Install using: pip install {pip_name})")
            all_passed = False

    return all_passed

def check_directories():
    print_header("3. Checking Required Project Directories")
    base = Path(__file__).resolve().parent
    required_dirs = [
        base / "app",
        base / "app" / "routes",
        base / "app" / "models",
        base / "app" / "static",
        base / "app" / "static" / "uploads" / "plant",
        base / "app" / "static" / "uploads" / "crop",
        base / "app" / "static" / "uploads" / "skin",
        base / "app" / "static" / "uploads" / "xray",
        base / "app" / "static" / "uploads" / "blood_reports",
        base / "app" / "templates",
        base / "ml_models" / "plant_model",
        base / "ml_models" / "crop_model",
        base / "ml_models" / "skin_model",
        base / "ml_models" / "xray_model",
        base / "database"
    ]

    all_ok = True
    for d in required_dirs:
        try:
            d.mkdir(parents=True, exist_ok=True)
            # Test write access
            test_file = d / ".write_test"
            test_file.write_text("ok")
            test_file.unlink()
            print(f" [OK] Directory verified: {d.relative_to(base)}")
        except Exception as e:
            print(f" [FAILED] Cannot write to {d.relative_to(base)}: {e}")
            all_ok = False
            
    return all_ok

def check_mysql():
    print_header("4. Checking MySQL / XAMPP Connection (Optional for Phase 1)")
    try:
        import pymysql
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            port=3306,
            connect_timeout=3
        )
        print(" [OK] Successfully connected to MySQL via XAMPP (Port 3306).")
        conn.close()
        return True
    except ImportError:
        print(" [INFO] pymysql is not installed yet. Skipping MySQL connection check.")
        return False
    except Exception as e:
        print(f" [NOTICE] Could not connect to MySQL: {e}")
        print("          If XAMPP is not running, start MySQL in the XAMPP Control Panel.")
        print("          (Note: MySQL is required in Phase 3 for database setup).")
        return False

def main():
    py_ok = check_python()
    pkg_ok = check_packages()
    dir_ok = check_directories()
    check_mysql()

    print_header("Summary")
    if dir_ok and pkg_ok:
        print(" ALL PHASE 1 CORE CHECKS PASSED!")
        print(" You are ready to run: python run.py")
    else:
        print(" Some requirements need attention.")
        print(" Follow the installation steps provided in the Phase 1 instructions.")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()

