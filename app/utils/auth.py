from functools import wraps
from flask import session, redirect, url_for, flash, request, abort

def login_required(f):
    """
    Decorator to ensure user is logged in before accessing private routes.
    Accepts both authenticated users and administrators.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id") and not session.get("admin_id") and not session.get("user_logged_in") and not session.get("admin_logged_in"):
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for("auth.login", next=request.endpoint))
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    """
    Decorator strictly for standard users.
    Redirects unauthenticated visitors to login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id") and not session.get("user_logged_in"):
            flash("Please sign in with your user account to access this page.", "warning")
            return redirect(url_for("auth.login", next=request.endpoint))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Strict Role-Based Access Control (RBAC) decorator for Administrator routes.
    - If not logged in -> redirects to Administrator login.
    - If logged in as standard user (role == 'user') -> returns HTTP 403 Forbidden.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 1. Check if user has admin privileges
        role = session.get("role")
        is_admin_session = session.get("admin_logged_in") is True or role == "admin"

        if is_admin_session:
            return f(*args, **kwargs)

        # 2. If logged in as a normal user -> Deny with HTTP 403 Forbidden
        if session.get("user_logged_in") or role == "user":
            abort(403)

        # 3. If unauthenticated -> Redirect to Admin Login
        flash("Administrator authentication required to access this console.", "warning")
        return redirect(url_for("admin.login"))

    return decorated_function

