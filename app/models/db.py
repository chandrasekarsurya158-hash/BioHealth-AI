import pymysql
from pymysql.cursors import DictCursor
from config import Config
from contextlib import contextmanager

def get_db_connection():
    """
    Creates and returns a connection to the MySQL database.
    Uses DictCursor so results are accessible via column names as dictionaries.
    """
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        port=Config.DB_PORT,
        cursorclass=DictCursor,
        autocommit=True,
        charset='utf8mb4'
    )

@contextmanager
def get_db():
    """
    Context manager for database transactions.
    Automatically closes the connection and handles rollbacks on exceptions.
    Usage:
        with get_db() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
    """
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        yield cursor
    except Exception as e:
        if connection:
            connection.rollback()
        raise e
    finally:
        if connection:
            connection.close()

def test_connection():
    """Returns True if MySQL is reachable and database exists, else False."""
    try:
        conn = get_db_connection()
        conn.close()
        return True
    except Exception:
        return False

