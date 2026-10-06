# database/connection.py
# Vital Forge - MySQL Connection

import mysql.connector
from mysql.connector import Error

from database.supabase_credentials import CredentialRetrievalError
from config import (
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_USER,
    get_mysql_password,
    MYSQL_DATABASE,
)


def _open_database_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=get_mysql_password(),
        database=MYSQL_DATABASE,
        autocommit=False,
        connection_timeout=20,
    )


def get_database_connection():
    """Connect directly to the Vital Forge MySQL database."""
    try:
        return _open_database_connection()
    except (CredentialRetrievalError, RuntimeError):
        print("Vital Forge database credential unavailable.")
        return None
    except Error:
        print("Vital Forge database connection failed.")
        return None


def check_database_connection() -> tuple[bool, str | None]:
    """Check the connection and return a safe diagnostic for startup display."""
    connection = None
    try:
        connection = _open_database_connection()
        if connection.is_connected():
            return True, None
        return False, "MySQL did not confirm the database connection."
    except CredentialRetrievalError as error:
        return False, str(error)
    except RuntimeError as error:
        return False, str(error)
    except Error:
        return False, (
            "Could not connect to MySQL. Check the host, port, database access, "
            "and network connection."
        )
    finally:
        if connection is not None:
            try:
                connection.close()
            except Error:
                pass


def test_connection():
    """Check whether Vital Forge can connect to MySQL."""
    connected, _ = check_database_connection()
    return connected


def close_connection(connection):
    """Safely close a MySQL connection."""
    if connection is not None:
        try:
            if connection.is_connected():
                connection.close()
        except Error:
            pass
