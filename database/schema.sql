-- =========================================================
-- Vital Forge - MySQL Database Schema
-- =========================================================

-- =========================================================
-- USERS
-- =========================================================

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_demo BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- USER PROFILES
-- =========================================================

CREATE TABLE IF NOT EXISTS profiles (
    profile_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,

    age INT NOT NULL,
    gender VARCHAR(30) NOT NULL,

    height_cm DECIMAL(6,2) NOT NULL,
    weight_kg DECIMAL(6,2) NOT NULL,

    activity_level VARCHAR(50) NOT NULL,

    water_goal_ml INT DEFAULT 2000,
    sleep_goal_hours DECIMAL(4,1) DEFAULT 8.0,
    steps_goal INT DEFAULT 8000,

    long_term_goal VARCHAR(50) NOT NULL,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);


-- =========================================================
-- DAILY TRACKING
-- =========================================================

CREATE TABLE IF NOT EXISTS daily_tracking (
    tracking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,

    tracking_date DATE NOT NULL,

    water_ml INT DEFAULT 0,
    steps INT DEFAULT 0,
    sleep_hours DECIMAL(4,1) DEFAULT 0,
    weight_kg DECIMAL(6,2) DEFAULT NULL,

    notes VARCHAR(500) DEFAULT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY unique_user_day (user_id, tracking_date),

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);


-- =========================================================
-- WORKOUTS
-- =========================================================

CREATE TABLE IF NOT EXISTS workouts (
    workout_id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(150) NOT NULL,
    description VARCHAR(500) NOT NULL,

    difficulty VARCHAR(30) NOT NULL,

    goal_weight_loss BOOLEAN DEFAULT FALSE,
    goal_weight_gain BOOLEAN DEFAULT FALSE,
    goal_muscular_build BOOLEAN DEFAULT FALSE,
    goal_general_fitness BOOLEAN DEFAULT FALSE,
    goal_endurance BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- DAILY WORKOUT ASSIGNMENTS
-- =========================================================

CREATE TABLE IF NOT EXISTS workout_assignments (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,
    workout_id INT NOT NULL,

    assignment_date DATE NOT NULL,

    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP NULL DEFAULT NULL,

    UNIQUE KEY unique_user_workout_day
        (user_id, assignment_date),

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    FOREIGN KEY (workout_id)
        REFERENCES workouts(workout_id)
        ON DELETE CASCADE
);


-- =========================================================
-- FOODS
-- =========================================================

CREATE TABLE IF NOT EXISTS foods (
    food_id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(150) NOT NULL UNIQUE,

    serving_size VARCHAR(100) NOT NULL,

    calories DECIMAL(7,2) NOT NULL,

    protein_g DECIMAL(7,2) DEFAULT 0,
    carbohydrates_g DECIMAL(7,2) DEFAULT 0,
    fat_g DECIMAL(7,2) DEFAULT 0,
    fiber_g DECIMAL(7,2) DEFAULT 0,

    category VARCHAR(50) DEFAULT 'Other'
);


-- =========================================================
-- FOOD LOG
-- =========================================================

CREATE TABLE IF NOT EXISTS food_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,
    food_id INT NOT NULL,

    log_date DATE NOT NULL,

    servings DECIMAL(6,2) DEFAULT 1,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    FOREIGN KEY (food_id)
        REFERENCES foods(food_id)
        ON DELETE CASCADE
);


-- =========================================================
-- USER GOAL PROGRESS
-- =========================================================

CREATE TABLE IF NOT EXISTS goal_progress (
    progress_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    progress_date DATE NOT NULL,

    progress_percentage DECIMAL(5,2) DEFAULT 0,

    note VARCHAR(500) DEFAULT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY unique_user_progress_day
        (user_id, progress_date),

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);


-- =========================================================
-- INDEXES
-- =========================================================

CREATE INDEX idx_tracking_user_date
ON daily_tracking(user_id, tracking_date);

CREATE INDEX idx_workout_assignment_user_date
ON workout_assignments(user_id, assignment_date);

-- =========================================================
-- WORKOUT EXERCISE CHECKLIST
-- =========================================================

CREATE TABLE IF NOT EXISTS workout_exercise_logs (
    exercise_log_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,
    exercise_date DATE NOT NULL,
    exercise_index TINYINT NOT NULL,
    exercise_name VARCHAR(150) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,

    UNIQUE KEY unique_user_exercise_day
        (user_id, exercise_date, exercise_index),

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_exercise_logs_user_date
ON workout_exercise_logs(user_id, exercise_date);

CREATE INDEX idx_food_name
ON foods(name);

CREATE INDEX idx_food_category
ON foods(category);

CREATE INDEX idx_food_logs_user_date
ON food_logs(user_id, log_date);

CREATE INDEX idx_goal_progress_user_date
ON goal_progress(user_id, progress_date);