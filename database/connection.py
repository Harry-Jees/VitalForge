# database/connection.py
# Vital Forge - MySQL Connection

import mysql.connector
from mysql.connector import Error

from config import (
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_DATABASE
)


def get_database_connection():
    """
    Connect directly to the Vital Forge MySQL database.
    """

    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )

        return connection

    except Error as error:
        print("Vital Forge database connection failed:", error)
        return None


def test_connection():
    """
    Check whether Vital Forge can connect to MySQL.
    """

    connection = get_database_connection()

    if connection is not None:
        try:
            if connection.is_connected():
                connection.close()
                return True

        except Error:
            pass

    return False


def close_connection(connection):
    """
    Safely close a MySQL connection.
    """

    if connection is not None:
        try:
            if connection.is_connected():
                connection.close()

        except Error:
            pass