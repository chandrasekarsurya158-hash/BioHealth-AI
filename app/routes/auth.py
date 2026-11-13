from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user import UserModel
from app.models.db import test_connection

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Page 3: User registration with MySQL database storage and hashing."""
    if request.method == "POST":
        fullname = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Validation checks
        if not fullname or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("auth/register.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "warning")
            return render_template("auth/register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "warning")
            return render_template("auth/register.html")

        if not test_connection():
            flash("Database connection unavailable. Please ensure MySQL is running in XAMPP.", "danger")
            return render_template("auth/register.html")

        try:
            user_id = UserModel.create_user(fullname, email, password)
            if user_id:
                flash("Account registered successfully! Please log in.", "success")
                return redirect(url_for("auth.login"))
            else:
                flash("An account with that email address already exists.", "warning")
        except Exception as e:
            flash(f"Registration error: {str(e)}", "danger")

    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Page 4: User authentication against MySQL users table."""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please enter both email and password.", "danger")
            return render_template("auth/login.html")

        if not test_connection():
            flash("Cannot connect to MySQL database. Please start MySQL in XAMPP.", "danger")
            return render_template("auth/login.html")

        try:
            user = UserModel.get_by_email(email)
            if user and UserModel.verify_password(user["password_hash"], password):
                user_role = user.get("role", "user")

                # Set secure session variables with role
                session.clear()
                session["user_id"] = user["id"]
                session["user_name"] = user["fullname"]
                session["user_email"] = user["email"]
                session["role"] = user_role

                if user_role == "admin":
                    session["admin_logged_in"] = True
                    session["admin_id"] = user["id"]
                    session["admin_name"] = user["fullname"]
                    flash(f"Administrator privileges verified: Welcome, {user['fullname']}.", "success")
                    return redirect(url_for("admin.dashboard"))
                else:
                    session["user_logged_in"] = True
                    flash(f"Welcome back, {user['fullname']}!", "success")
                    next_page = request.args.get("next")
                    return redirect(url_for(next_page) if next_page else url_for("dashboard.user_dashboard"))
            else:
                flash("Invalid email address or password.", "danger")
        except Exception as e:
            flash(f"Login error: {str(e)}", "danger")

    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    """Destroys current user session."""
    session.clear()
    flash("You have been securely logged out.", "info")
    return redirect(url_for("auth.login"))
