import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "fitbuddy.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            name TEXT,
            age INTEGER,
            weight REAL,
            goal TEXT,
            intensity TEXT,
            original_plan TEXT,
            updated_plan TEXT,
            feedback TEXT,
            nutrition_tip TEXT NOT NULL DEFAULT ''
        )
    """)

    conn.commit()
    conn.close()

    print("Database initialized successfully")


def save_user_plan(
    user_id,
    name,
    age,
    weight,
    goal,
    intensity,
    original_plan
):
    conn = get_connection()
    cursor = conn.cursor()

    print("========== SAVE USER ==========")
    print("USER ID:", user_id)
    print("NAME:", name)
    print("AGE:", age)
    print("WEIGHT:", weight)
    print("GOAL:", goal)
    print("INTENSITY:", intensity)

    # Check whether this user already exists
    cursor.execute("""
        SELECT id
        FROM users
        WHERE user_id = ?
    """, (user_id,))

    existing_user = cursor.fetchone()

    if existing_user:

        # User already exists → UPDATE
        cursor.execute("""
            UPDATE users
            SET
                name = ?,
                age = ?,
                weight = ?,
                goal = ?,
                intensity = ?,
                original_plan = ?
            WHERE user_id = ?
        """, (
            name,
            age,
            weight,
            goal,
            intensity,
            original_plan,
            user_id
        ))

        print("EXISTING USER UPDATED:", user_id)

    else:

        # New user → INSERT
        cursor.execute("""
            INSERT INTO users
            (
                user_id,
                name,
                age,
                weight,
                goal,
                intensity,
                original_plan,
                updated_plan,
                feedback,
                nutrition_tip
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            name,
            age,
            weight,
            goal,
            intensity,
            original_plan,
            "",
            "",
            ""
        ))

        print("NEW USER SAVED:", user_id)

    conn.commit()
    conn.close()

def save_feedback(user_id, feedback):
    conn = get_connection()
    cursor = conn.cursor()

    # Get the user's current details
    cursor.execute("""
        SELECT name, goal, intensity, original_plan
        FROM users
        WHERE user_id = ?
    """, (user_id,))

    user = cursor.fetchone()

    if not user:
        conn.close()
        raise Exception("User ID not found")

    name = user["name"]
    goal = user["goal"]
    intensity = user["intensity"]

    # Create updated workout plan based on feedback
    updated_plan = f"""
Updated 7-Day Workout Plan

User: {name}
Goal: {goal}
Intensity: {intensity}

Feedback considered:
{feedback}

Day 1 – Full Body
Squats – 3 × 12
Push-ups – 3 × 10
Lunges – 3 × 10
Plank – 3 × 30 sec

Day 2 – Upper Body
Push-ups – 3 × 10
Shoulder Press – 3 × 12
Biceps Curls – 3 × 12
Triceps Dips – 3 × 10

Day 3 – Lower Body
Squats – 3 × 15
Lunges – 3 × 12
Glute Bridges – 3 × 15
Calf Raises – 3 × 15

Day 4 – Cardio
Jumping Jacks – 3 × 30 sec
High Knees – 3 × 30 sec
Mountain Climbers – 3 × 20
Brisk Walking – 20 minutes

Day 5 – Core
Crunches – 3 × 15
Leg Raises – 3 × 12
Russian Twists – 3 × 15
Plank – 3 × 40 sec

Day 6 – Full Body
Squats – 3 × 12
Push-ups – 3 × 10
Burpees – 3 × 8
Plank – 3 × 30 sec

Day 7 – Rest & Recovery
Light Walking – 20 minutes
Full Body Stretching – 10 minutes
Deep Breathing – 5 minutes
"""

    # Save feedback + updated plan
    cursor.execute("""
        UPDATE users
        SET
            feedback = ?,
            updated_plan = ?
        WHERE user_id = ?
    """, (
        feedback,
        updated_plan,
        user_id
    ))

    conn.commit()
    conn.close()

    print("FEEDBACK SAVED:", user_id)
    print("UPDATED PLAN SAVED:", user_id)

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            user_id,
            name,
            age,
            weight,
            goal,
            intensity,
            original_plan,
            updated_plan,
            feedback,
            nutrition_tip
        FROM users
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    users = [dict(row) for row in rows]

    conn.close()

    print("DATABASE PATH:", DB_PATH)
    print("TOTAL USERS:", len(users))
    print("USERS:", users)

    return users