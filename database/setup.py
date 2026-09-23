# database/setup.py
# Vital Forge
# Creates the MySQL database, tables, and initial application data.

import os
import sys

# Allow this file to be run directly from the database folder.
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import mysql.connector

from config import (
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_DATABASE,
)

from data import FOODS, WORKOUTS


# ---------------------------------------------------------
# CONNECTION
# ---------------------------------------------------------

def get_server_connection():
    """Connect to MySQL without selecting the Vital Forge database."""

    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD
    )


def get_database_connection():
    """Connect directly to the Vital Forge database."""

    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )


# ---------------------------------------------------------
# CREATE DATABASE
# ---------------------------------------------------------

def create_database():
    """Create the Vital Forge database if it does not exist."""

    connection = get_server_connection()
    cursor = connection.cursor()

    cursor.execute(
        f"""
        CREATE DATABASE IF NOT EXISTS `{MYSQL_DATABASE}`
        CHARACTER SET utf8mb4
        COLLATE utf8mb4_unicode_ci
        """
    )

    connection.commit()

    cursor.close()
    connection.close()


# ---------------------------------------------------------
# CREATE TABLES
# ---------------------------------------------------------

def create_tables():
    """Create all database tables using schema.sql."""

    schema_path = os.path.join(
        PROJECT_ROOT,
        "database",
        "schema.sql"
    )

    with open(
        schema_path,
        "r",
        encoding="utf-8"
    ) as file:
        schema = file.read()

    connection = get_database_connection()
    cursor = connection.cursor()

    # Remove SQL comments.
    cleaned_lines = []

    for line in schema.splitlines():
        stripped = line.strip()

        if stripped.startswith("--"):
            continue

        cleaned_lines.append(line)

    cleaned_schema = "\n".join(cleaned_lines)

    # Split the schema into individual SQL statements.
    statements = cleaned_schema.split(";")

    for statement in statements:
        statement = statement.strip()

        if not statement:
            continue

        # The database name is already selected through the connection.
        if statement.upper().startswith("CREATE DATABASE"):
            continue

        if statement.upper().startswith("USE "):
            continue

        try:
            cursor.execute(statement)
        except mysql.connector.Error as error:
            print("\nSchema statement failed:")
            print(statement[:250])
            print(f"\nMySQL error: {error}\n")

            cursor.close()
            connection.close()
            raise

    connection.commit()

    cursor.close()
    connection.close()


# ---------------------------------------------------------
# SEED FOODS
# ---------------------------------------------------------

def seed_foods():
    """Insert the default food library."""

    connection = get_database_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO foods
        (
            name,
            serving_size,
            calories,
            protein_g,
            carbohydrates_g,
            fat_g,
            fiber_g,
            category
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s, %s
        )
        ON DUPLICATE KEY UPDATE
            serving_size = VALUES(serving_size),
            calories = VALUES(calories),
            protein_g = VALUES(protein_g),
            carbohydrates_g = VALUES(carbohydrates_g),
            fat_g = VALUES(fat_g),
            fiber_g = VALUES(fiber_g),
            category = VALUES(category)
    """

    values = []

    for food in FOODS:
        values.append(
            (
                food["name"],
                food["serving_size"],
                food["calories"],
                food["protein_g"],
                food["carbohydrates_g"],
                food["fat_g"],
                food["fiber_g"],
                food["category"],
            )
        )

    cursor.executemany(
        query,
        values
    )

    connection.commit()

    cursor.close()
    connection.close()

    print(
        f"Foods seeded successfully: {len(values)}"
    )


# ---------------------------------------------------------
# SEED WORKOUTS
# ---------------------------------------------------------

def seed_workouts():
    """Insert the default workout library."""

    connection = get_database_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO workouts
        (
            name,
            description,
            difficulty,
            goal_weight_loss,
            goal_weight_gain,
            goal_muscular_build,
            goal_general_fitness,
            goal_endurance
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s, %s
        )
        ON DUPLICATE KEY UPDATE
            description = VALUES(description),
            difficulty = VALUES(difficulty),
            goal_weight_loss = VALUES(goal_weight_loss),
            goal_weight_gain = VALUES(goal_weight_gain),
            goal_muscular_build = VALUES(goal_muscular_build),
            goal_general_fitness = VALUES(goal_general_fitness),
            goal_endurance = VALUES(goal_endurance)
    """

    values = []

    for workout in WORKOUTS:
        goals = workout["goals"]

        values.append(
            (
                workout["name"],
                workout["description"],
                workout["difficulty"],
                "Weight loss" in goals,
                "Weight gain" in goals,
                "Muscular build" in goals,
                "General fitness" in goals,
                "Endurance" in goals,
            )
        )

    cursor.executemany(
        query,
        values
    )

    connection.commit()

    cursor.close()
    connection.close()

    print(
        f"Workouts seeded successfully: {len(values)}"
    )


# ---------------------------------------------------------
# VERIFY SEEDING
# ---------------------------------------------------------

def verify_seed_data():
    """Check that the required default data exists."""

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM foods"
    )
    food_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM workouts"
    )
    workout_count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    print(
        f"Food records in database: {food_count}"
    )
    print(
        f"Workout records in database: {workout_count}"
    )

    if food_count < 300:
        raise RuntimeError(
            "Database contains fewer than 300 foods."
        )

    if workout_count < 25:
        raise RuntimeError(
            "Database contains fewer than 25 workouts."
        )


# ---------------------------------------------------------
# MAIN SETUP
# ---------------------------------------------------------

def setup_database():
    """Run the complete Vital Forge database setup."""

    print("=" * 55)
    print("VITAL FORGE DATABASE SETUP")
    print("=" * 55)

    print("\n1. Creating database...")
    create_database()
    print("Database ready.")

    print("\n2. Creating tables...")
    create_tables()
    print("Tables ready.")

    print("\n3. Seeding foods...")
    seed_foods()

    print("\n4. Seeding workouts...")
    seed_workouts()

    print("\n5. Verifying data...")
    verify_seed_data()

    print("\n" + "=" * 55)
    print("DATABASE SETUP COMPLETE")
    print("=" * 55)


# ---------------------------------------------------------
# RUN DIRECTLY
# ---------------------------------------------------------

if __name__ == "__main__":
    try:
        setup_database()

    except mysql.connector.Error as error:
        print("\nMySQL ERROR:")
        print(error)
        print(
            "\nCheck your MySQL server, username, password, "
            "and settings in config.py."
        )

    except Exception as error:
        print("\nSETUP ERROR:")
        print(error)