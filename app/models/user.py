from werkzeug.security import generate_password_hash, check_password_hash
from app.models.db import get_db

class UserModel:
    """Handles all user database operations with secure password hashing."""

    @staticmethod
    def create_user(fullname, email, password):
        """
        Hashes password using PBKDF2:SHA256 and inserts new user into MySQL.
        Returns newly generated user id, or None if email already exists.
        """
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        with get_db() as cursor:
            # Check for existing email
            cursor.execute("SELECT id FROM users WHERE email = %s", (email.lower(),))
            if cursor.fetchone():
                return None
            
            cursor.execute(
                "INSERT INTO users (fullname, email, role, password_hash) VALUES (%s, %s, 'user', %s)",
                (fullname, email.lower(), password_hash)
            )
            return cursor.lastrowid

    @staticmethod
    def get_by_email(email):
        """Retrieves user record by email address including role."""
        with get_db() as cursor:
            cursor.execute(
                "SELECT id, fullname, email, role, password_hash, created_at FROM users WHERE email = %s",
                (email.lower(),)
            )
            return cursor.fetchone()

    @staticmethod
    def get_by_id(user_id):
        """Retrieves user record by primary key id including role."""
        with get_db() as cursor:
            cursor.execute(
                "SELECT id, fullname, email, role, created_at FROM users WHERE id = %s",
                (user_id,)
            )
            return cursor.fetchone()

    @staticmethod
    def verify_password(stored_hash, candidate_password):
        """Securely compares password against stored PBKDF2 hash."""
        return check_password_hash(stored_hash, candidate_password)

    @staticmethod
    def update_profile(user_id, fullname, email):
        """Updates user profile information."""
        with get_db() as cursor:
            cursor.execute(
                "UPDATE users SET fullname = %s, email = %s WHERE id = %s",
                (fullname, email.lower(), user_id)
            )
            return True

    @staticmethod
    def update_password(user_id, new_password):
        """Hashes new password and updates user record."""
        new_hash = generate_password_hash(new_password, method='pbkdf2:sha256')
        with get_db() as cursor:
            cursor.execute(
                "UPDATE users SET password_hash = %s WHERE id = %s",
                (new_hash, user_id)
            )
            return True

    @staticmethod
    def delete_account(user_id):
        """Deletes user account (cascades to all user records)."""
        with get_db() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            return True

    @staticmethod
    def get_dashboard_counts(user_id):
        """Fetches scan counts for user dashboard cards."""
        with get_db() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM plant_detection_results WHERE user_id = %s", (user_id,))
            plant_count = cursor.fetchone()["count"]
            
            cursor.execute("SELECT COUNT(*) as count FROM crop_detection_results WHERE user_id = %s", (user_id,))
            crop_count = cursor.fetchone()["count"]
            
            cursor.execute("SELECT COUNT(*) as count FROM skin_screening_results WHERE user_id = %s", (user_id,))
            skin_count = cursor.fetchone()["count"]
            
            cursor.execute("SELECT COUNT(*) as count FROM blood_reports WHERE user_id = %s", (user_id,))
            blood_count = cursor.fetchone()["count"]
            
            cursor.execute("SELECT COUNT(*) as count FROM xray_results WHERE user_id = %s", (user_id,))
            xray_count = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) as count FROM symptom_assessments WHERE user_id = %s", (user_id,))
            symptoms_count = cursor.fetchone()["count"]

            return {
                "plant": plant_count,
                "crop": crop_count,
                "skin": skin_count,
                "blood": blood_count,
                "xray": xray_count,
                "symptoms": symptoms_count,
                "total": plant_count + crop_count + skin_count + blood_count + xray_count + symptoms_count
            }

    @staticmethod
    def get_all_users():
        """Fetches all registered users with their individual activity counts for Admin management."""
        with get_db() as cursor:
            cursor.execute("""
                SELECT u.id, u.fullname, u.email, u.role, u.created_at,
                       (SELECT COUNT(*) FROM analysis_history WHERE user_id = u.id) AS scan_count
                FROM users u
                ORDER BY u.created_at DESC
            """)
            return cursor.fetchall()

    @staticmethod
    def update_user_role(user_id, new_role):
        """Updates user authorization role ('user' or 'admin')."""
        if new_role not in ("user", "admin"):
            return False
        with get_db() as cursor:
            cursor.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
            return True

