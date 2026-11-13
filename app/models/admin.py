from werkzeug.security import generate_password_hash, check_password_hash
from app.models.db import get_db

class AdminModel:
    """Handles administrator account lookup and system statistics."""

    @staticmethod
    def get_by_username(username):
        """Finds admin by username."""
        with get_db() as cursor:
            cursor.execute(
                "SELECT id, username, password_hash, fullname, email FROM admins WHERE username = %s",
                (username,)
            )
            return cursor.fetchone()

    @staticmethod
    def verify_password(stored_hash, candidate_password):
        """Securely verifies admin password hash."""
        return check_password_hash(stored_hash, candidate_password)

    @staticmethod
    def get_system_analytics():
        """Fetches aggregate numbers across all users and modules for Admin Dashboard."""
        with get_db() as cursor:
            cursor.execute("SELECT COUNT(*) as total_users FROM users")
            total_users = cursor.fetchone()["total_users"]

            cursor.execute("SELECT COUNT(*) as total_plant FROM plant_detection_results")
            total_plant = cursor.fetchone()["total_plant"]

            cursor.execute("SELECT COUNT(*) as total_crop FROM crop_detection_results")
            total_crop = cursor.fetchone()["total_crop"]

            cursor.execute("SELECT COUNT(*) as total_skin FROM skin_screening_results")
            total_skin = cursor.fetchone()["total_skin"]

            cursor.execute("SELECT COUNT(*) as total_xray FROM xray_results")
            total_xray = cursor.fetchone()["total_xray"]

            cursor.execute("SELECT COUNT(*) as total_blood FROM blood_reports")
            total_blood = cursor.fetchone()["total_blood"]

            cursor.execute("SELECT COUNT(*) as total_symptoms FROM symptom_assessments")
            total_symptoms = cursor.fetchone()["total_symptoms"]

            cursor.execute("SELECT COUNT(*) as total_medicines FROM medicines")
            total_medicines = cursor.fetchone()["total_medicines"]

            return {
                "total_users": total_users,
                "total_scans": total_plant + total_crop + total_skin + total_xray + total_blood + total_symptoms,
                "plant_scans": total_plant,
                "crop_scans": total_crop,
                "skin_scans": total_skin,
                "xray_scans": total_xray,
                "blood_scans": total_blood,
                "symptoms_scans": total_symptoms,
                "total_medicines": total_medicines
            }

    @staticmethod
    def log_activity(admin_id, admin_name, action, target_module, details="", ip_address=""):
        """Records an administrative event to the audit trail."""
        try:
            with get_db() as cursor:
                cursor.execute(
                    """INSERT INTO admin_activity_logs (admin_id, admin_name, action, target_module, details, ip_address)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (admin_id, admin_name, action, target_module, details, ip_address)
                )
        except Exception as e:
            print(f"Notice: Failed to write admin activity log: {e}")

    @staticmethod
    def get_recent_logs(limit=15):
        """Fetches the latest admin system activity logs."""
        try:
            with get_db() as cursor:
                cursor.execute(
                    """SELECT id, admin_id, admin_name, action, target_module, details, ip_address, created_at
                       FROM admin_activity_logs
                       ORDER BY created_at DESC
                       LIMIT %s""",
                    (limit,)
                )
                return cursor.fetchall()
        except Exception:
            return []

    @staticmethod
    def get_all_medicines():
        """Fetches all medicines from MySQL for admin review."""
        try:
            with get_db() as cursor:
                cursor.execute(
                    """SELECT id, name, generic_name, brand_examples, category, prescription_type, uses, precautions
                       FROM medicines
                       ORDER BY name ASC"""
                )
                return cursor.fetchall()
        except Exception:
            return []

    @staticmethod
    def add_medicine(name, generic_name, brand_examples, category, prescription_type, uses, precautions, warnings="", side_effects="", contraindications=""):
        """Inserts a new medicine record into MySQL."""
        with get_db() as cursor:
            cursor.execute(
                """INSERT INTO medicines (name, generic_name, brand_examples, category, prescription_type, uses, precautions, warnings, side_effects, contraindications)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (name, generic_name, brand_examples, category, prescription_type, uses, precautions, warnings, side_effects, contraindications)
            )
            return cursor.lastrowid

    @staticmethod
    def delete_medicine(med_id):
        """Deletes a medicine record from MySQL."""
        with get_db() as cursor:
            cursor.execute("DELETE FROM medicines WHERE id = %s", (med_id,))
            return True

