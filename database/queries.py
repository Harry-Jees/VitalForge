# database/queries.py
# Vital Forge
# All MySQL queries used by the application.

from datetime import date, timedelta

from database.connection import get_database_connection


# ---------------------------------------------------------
# Generic database helpers
# ---------------------------------------------------------

def fetch_one(query, params=None):
    """Run a SELECT query and return one row as a dictionary."""
    connection = get_database_connection()

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchone()
        cursor.close()
        return result

    finally:
        connection.close()


def fetch_all(query, params=None):
    """Run a SELECT query and return all rows as dictionaries."""
    connection = get_database_connection()

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        cursor.close()
        return results

    finally:
        connection.close()


def execute_query(query, params=None):
    """Run an INSERT, UPDATE, or DELETE query."""
    connection = get_database_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        connection.commit()

        affected_rows = cursor.rowcount

        cursor.close()
        return affected_rows

    finally:
        connection.close()


def execute_insert(query, params=None):
    """Run an INSERT query and return the new row ID."""
    connection = get_database_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        connection.commit()

        inserted_id = cursor.lastrowid

        cursor.close()
        return inserted_id

    finally:
        connection.close()


# ---------------------------------------------------------
# Users
# ---------------------------------------------------------

def get_user_by_email(email):
    """Find a user using their email address."""
    query = """
        SELECT *
        FROM users
        WHERE email = %s
        LIMIT 1
    """

    return fetch_one(query, (email,))


def get_user_by_id(user_id):
    """Find a user using their user ID."""
    query = """
        SELECT *
        FROM users
        WHERE user_id = %s
        LIMIT 1
    """

    return fetch_one(query, (user_id,))


def create_user(name, email, password_hash, is_demo=False):
    """Create a new user and return the generated user ID."""
    query = """
        INSERT INTO users
            (name, email, password_hash, is_demo)
        VALUES
            (%s, %s, %s, %s)
    """

    return execute_insert(
        query,
        (name, email, password_hash, is_demo)
    )


# ---------------------------------------------------------
# Profile
# ---------------------------------------------------------

def save_profile(user_id, profile):
    """Create or update a user's fitness profile."""
    query = """
        INSERT INTO profiles
            (
                user_id,
                age,
                gender,
                height_cm,
                weight_kg,
                activity_level,
                water_goal_ml,
                sleep_goal_hours,
                steps_goal,
                long_term_goal
            )
        VALUES
            (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
        ON DUPLICATE KEY UPDATE
            age = VALUES(age),
            gender = VALUES(gender),
            height_cm = VALUES(height_cm),
            weight_kg = VALUES(weight_kg),
            activity_level = VALUES(activity_level),
            water_goal_ml = VALUES(water_goal_ml),
            sleep_goal_hours = VALUES(sleep_goal_hours),
            steps_goal = VALUES(steps_goal),
            long_term_goal = VALUES(long_term_goal)
    """

    params = (
        user_id,
        profile["age"],
        profile["gender"],
        profile["height_cm"],
        profile["weight_kg"],
        profile["activity_level"],
        profile["water_goal_ml"],
        profile["sleep_goal_hours"],
        profile["steps_goal"],
        profile["long_term_goal"]
    )

    return execute_query(query, params)


def get_profile(user_id):
    """Get the fitness profile of a user."""
    query = """
        SELECT *
        FROM profiles
        WHERE user_id = %s
        LIMIT 1
    """

    return fetch_one(query, (user_id,))


# ---------------------------------------------------------
# Daily tracking
# ---------------------------------------------------------

def get_daily_tracking(user_id, tracking_date=None):
    """Get tracking information for a specific day."""
    if tracking_date is None:
        tracking_date = date.today()

    query = """
        SELECT *
        FROM daily_tracking
        WHERE user_id = %s
          AND tracking_date = %s
        LIMIT 1
    """

    return fetch_one(
        query,
        (user_id, tracking_date)
    )


def save_daily_tracking(user_id, tracking):
    """Create or update daily tracking information."""
    tracking_date = tracking.get(
        "tracking_date",
        date.today()
    )

    query = """
        INSERT INTO daily_tracking
            (
                user_id,
                tracking_date,
                water_ml,
                steps,
                sleep_hours,
                weight_kg,
                notes
            )
        VALUES
            (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            water_ml = VALUES(water_ml),
            steps = VALUES(steps),
            sleep_hours = VALUES(sleep_hours),
            weight_kg = VALUES(weight_kg),
            notes = VALUES(notes)
    """

    params = (
        user_id,
        tracking_date,
        tracking.get("water_ml", 0),
        tracking.get("steps", 0),
        tracking.get("sleep_hours", 0),
        tracking.get("weight_kg"),
        tracking.get("notes", "")
    )

    return execute_query(query, params)


def get_tracking_history(user_id, days=30):
    """Get recent daily tracking history."""
    try:
        days = int(days)
    except (TypeError, ValueError):
        days = 30

    days = max(1, min(days, 365))

    query = """
        SELECT *
        FROM daily_tracking
        WHERE user_id = %s
          AND tracking_date >= %s
        ORDER BY tracking_date ASC
    """

    start_date = date.today() - timedelta(days=days - 1)

    return fetch_all(
        query,
        (user_id, start_date)
    )


# ---------------------------------------------------------
# Workouts
# ---------------------------------------------------------

def get_all_workouts():
    """Return every workout in the database."""
    query = """
        SELECT *
        FROM workouts
        ORDER BY workout_id ASC
    """

    return fetch_all(query)


def get_workout_by_id(workout_id):
    """Find a workout by its ID."""
    query = """
        SELECT *
        FROM workouts
        WHERE workout_id = %s
        LIMIT 1
    """

    return fetch_one(query, (workout_id,))


def get_workouts_for_goal(goal):
    """
    Return workouts suitable for a specific long-term goal.

    The goal column is selected only from this whitelist.
    This prevents the goal value from becoming raw SQL.
    """

    goal_columns = {
        "Weight loss": "goal_weight_loss",
        "Weight gain": "goal_weight_gain",
        "Muscular build": "goal_muscular_build",
        "General fitness": "goal_general_fitness",
        "Endurance": "goal_endurance"
    }

    column = goal_columns.get(goal)

    if column is None:
        return get_all_workouts()

    query = f"""
        SELECT *
        FROM workouts
        WHERE {column} = TRUE
        ORDER BY workout_id ASC
    """

    return fetch_all(query)


# ---------------------------------------------------------
# Workout assignments
# ---------------------------------------------------------

def get_today_workout(user_id, assignment_date=None):
    """Get the workout assigned to a user for a particular day."""
    if assignment_date is None:
        assignment_date = date.today()

    query = """
        SELECT
            wa.assignment_id,
            wa.user_id,
            wa.workout_id,
            wa.assignment_date,
            wa.completed,
            wa.completed_at,
            w.name,
            w.description,
            w.difficulty,
            w.goal_weight_loss,
            w.goal_weight_gain,
            w.goal_muscular_build,
            w.goal_general_fitness,
            w.goal_endurance
        FROM workout_assignments wa
        INNER JOIN workouts w
            ON wa.workout_id = w.workout_id
        WHERE wa.user_id = %s
          AND wa.assignment_date = %s
        LIMIT 1
    """

    return fetch_one(
        query,
        (user_id, assignment_date)
    )


def get_exercise_logs(user_id, exercise_date=None):
    """Return checklist state for one user's workout date."""
    if exercise_date is None:
        exercise_date = date.today()

    query = """
        SELECT exercise_index, exercise_name, completed
        FROM workout_exercise_logs
        WHERE user_id = %s
          AND exercise_date = %s
        ORDER BY exercise_index ASC
    """

    return fetch_all(query, (user_id, exercise_date))


def save_exercise_log(
    user_id,
    exercise_date,
    exercise_index,
    exercise_name,
    completed,
):
    """Insert or update one exercise checklist item."""
    query = """
        INSERT INTO workout_exercise_logs
            (user_id, exercise_date, exercise_index, exercise_name, completed)
        VALUES
            (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            exercise_name = VALUES(exercise_name),
            completed = VALUES(completed)
    """

    return execute_query(
        query,
        (user_id, exercise_date, exercise_index, exercise_name, completed),
    )


def assign_workout(
    user_id,
    workout_id,
    assignment_date=None
):
    """
    Assign a workout to a user for a day.

    If a workout is already assigned for that day,
    the existing assignment is kept.
    """

    if assignment_date is None:
        assignment_date = date.today()

    existing = get_today_workout(
        user_id,
        assignment_date
    )

    if existing:
        return existing["assignment_id"]

    query = """
        INSERT INTO workout_assignments
            (
                user_id,
                workout_id,
                assignment_date,
                completed
            )
        VALUES
            (%s, %s, %s, FALSE)
    """

    return execute_insert(
        query,
        (
            user_id,
            workout_id,
            assignment_date
        )
    )


def complete_workout(
    user_id,
    assignment_date=None,
    completed=True
):
    """Mark the assigned workout as completed or incomplete."""
    if assignment_date is None:
        assignment_date = date.today()

    if completed:
        query = """
            UPDATE workout_assignments
            SET
                completed = TRUE,
                completed_at = NOW()
            WHERE user_id = %s
              AND assignment_date = %s
        """
    else:
        query = """
            UPDATE workout_assignments
            SET
                completed = FALSE,
                completed_at = NULL
            WHERE user_id = %s
              AND assignment_date = %s
        """

    return execute_query(
        query,
        (user_id, assignment_date)
    )


def get_workout_history(user_id, days=30):
    """Get recent workout completion history."""
    try:
        days = int(days)
    except (TypeError, ValueError):
        days = 30

    days = max(1, min(days, 365))

    start_date = date.today() - timedelta(days=days - 1)

    query = """
        SELECT
            wa.assignment_id,
            wa.assignment_date,
            wa.completed,
            wa.completed_at,
            w.name AS workout_name,
            w.difficulty
        FROM workout_assignments wa
        INNER JOIN workouts w
            ON wa.workout_id = w.workout_id
        WHERE wa.user_id = %s
          AND wa.assignment_date >= %s
        ORDER BY wa.assignment_date ASC
    """

    return fetch_all(
        query,
        (user_id, start_date)
    )


# ---------------------------------------------------------
# Foods
# ---------------------------------------------------------

def search_foods(search_text="", limit=30):
    """Search the food database by name."""
    try:
        limit = int(limit)
    except (TypeError, ValueError):
        limit = 30

    limit = max(1, min(limit, 100))

    search_text = (search_text or "").strip()

    if search_text:
        query = """
            SELECT *
            FROM foods
            WHERE name LIKE %s
            ORDER BY name ASC
            LIMIT %s
        """

        return fetch_all(
            query,
            (f"%{search_text}%", limit)
        )

    query = """
        SELECT *
        FROM foods
        ORDER BY name ASC
        LIMIT %s
    """

    return fetch_all(query, (limit,))


def get_food_by_id(food_id):
    """Find a food using its database ID."""
    query = """
        SELECT *
        FROM foods
        WHERE food_id = %s
        LIMIT 1
    """

    return fetch_one(query, (food_id,))


def add_food_log(
    user_id,
    food_id,
    log_date=None,
    servings=1
):
    """Add a food entry to a user's food log."""
    if log_date is None:
        log_date = date.today()

    query = """
        INSERT INTO food_logs
            (
                user_id,
                food_id,
                log_date,
                servings
            )
        VALUES
            (%s, %s, %s, %s)
    """

    return execute_insert(
        query,
        (
            user_id,
            food_id,
            log_date,
            servings
        )
    )


def get_food_logs(user_id, log_date=None):
    """Get food logs, optionally for one specific day."""
    if log_date is None:
        log_date = date.today()

    query = """
        SELECT
            fl.log_id AS food_log_id,
            fl.user_id,
            fl.food_id,
            fl.log_date,
            fl.servings,
            f.name,
            f.serving_size,
            f.calories,
            f.protein_g,
            f.carbohydrates_g,
            f.fat_g,
            f.fiber_g,
            f.category
        FROM food_logs fl
        INNER JOIN foods f
            ON fl.food_id = f.food_id
        WHERE fl.user_id = %s
          AND fl.log_date = %s
        ORDER BY fl.log_id DESC
    """

    return fetch_all(
        query,
        (user_id, log_date)
    )


def delete_food_log(log_id, user_id):
    """Delete a specific food log entry for a user."""
    query = """
        DELETE FROM food_logs
        WHERE log_id = %s
          AND user_id = %s
    """

    return execute_query(query, (log_id, user_id))


def create_custom_food(
    name,
    serving_size,
    calories,
    protein_g=0,
    carbohydrates_g=0,
    fat_g=0,
    fiber_g=0,
    category="Custom"
):
    """Add a new custom food item to the database."""
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
            (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    return execute_insert(
        query,
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
    )


# ---------------------------------------------------------
# Goal progress
# ---------------------------------------------------------

def save_goal_progress(
    user_id,
    progress_value,
    progress_date=None
):
    """Save or update a user's goal progress percentage."""
    if progress_date is None:
        progress_date = date.today()

    try:
        query = """
            INSERT INTO goal_progress
                (user_id, progress_date, progress_percentage)
            VALUES
                (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                progress_percentage = VALUES(progress_percentage)
        """
        return execute_query(query, (user_id, progress_date, progress_value))
    except Exception:
        query = """
            INSERT INTO goal_progress
                (user_id, progress_date, progress_value)
            VALUES
                (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                progress_value = VALUES(progress_value)
        """
        return execute_query(query, (user_id, progress_date, progress_value))


def get_goal_progress(user_id, days=30):
    """Get recent goal progress."""
    try:
        days = int(days)
    except (TypeError, ValueError):
        days = 30

    days = max(1, min(days, 365))

    start_date = date.today() - timedelta(days=days - 1)

    query = """
        SELECT *
        FROM goal_progress
        WHERE user_id = %s
          AND progress_date >= %s
        ORDER BY progress_date ASC
    """

    return fetch_all(
        query,
        (user_id, start_date)
    )