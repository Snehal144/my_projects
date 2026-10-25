import sqlite3
from datetime import date, timedelta
from pathlib import Path

import streamlit as st

DB_PATH = Path(__file__).with_name("habits.db")
DEFAULT_HABITS = [
    "Drink water",
    "Exercise",
    "Read",
    "Meditate",
    "Sleep 8 hours",
]


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS completions (
                habit_id INTEGER NOT NULL,
                completion_date TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (habit_id, completion_date),
                FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
            )
        """)


def get_habits():
    with get_connection() as connection:
        return connection.execute(
            "SELECT id, name FROM habits ORDER BY name"
        ).fetchall()


initialize_database()

st.title("Habit Tracker")

add_tab, track_tab, progress_tab = st.tabs(
    ["Add Habits", "Track Habits", "Progress"]
)

with add_tab:
    st.header("Add habits")

    selected_defaults = st.multiselect(
        "Choose from default habits",
        DEFAULT_HABITS,
    )

    if st.button("Add selected default habits"):
        with get_connection() as connection:
            connection.executemany(
                "INSERT OR IGNORE INTO habits (name) VALUES (?)",
                [(name,) for name in selected_defaults],
            )
        st.success("Selected habits added.")
        st.rerun()

    st.subheader("Add a custom habit")
    with st.form("custom_habit_form", clear_on_submit=True):
        custom_habit = st.text_input("Habit name")
        submitted = st.form_submit_button("Add custom habit")

    if submitted:
        name = custom_habit.strip()
        if not name:
            st.error("Enter a habit name.")
        else:
            with get_connection() as connection:
                connection.execute(
                    "INSERT OR IGNORE INTO habits (name) VALUES (?)",
                    (name,),
                )
            st.success(f'"{name}" added.')
            st.rerun()

    habits = get_habits()
    st.subheader("Your habits")
    if habits:
        for _, name in habits:
            st.write(f"• {name}")
    else:
        st.info("You haven't added any habits yet.")

with track_tab:
    st.header(f"Track habits — {date.today().strftime('%B %d, %Y')}")
    habits = get_habits()

    if not habits:
        st.info("Add habits first using the Add Habits tab.")
    else:
        today = date.today().isoformat()

        with get_connection() as connection:
            saved = dict(connection.execute(
                """
                SELECT habit_id, completed
                FROM completions
                WHERE completion_date = ?
                """,
                (today,),
            ).fetchall())

        with st.form("track_habits_form"):
            checked = {}
            for habit_id, name in habits:
                checked[habit_id] = st.checkbox(
                    name,
                    value=bool(saved.get(habit_id, 0)),
                    key=f"habit_{habit_id}",
                )

            submitted = st.form_submit_button("Save today's progress")

        if submitted:
            with get_connection() as connection:
                connection.executemany(
                    """
                    INSERT OR REPLACE INTO completions
                        (habit_id, completion_date, completed)
                    VALUES (?, ?, ?)
                    """,
                    [
                        (habit_id, today, int(is_checked))
                        for habit_id, is_checked in checked.items()
                    ],
                )
            st.success("Today's progress saved.")
            st.rerun()

with progress_tab:
    st.header("Progress")
    habits = get_habits()

    if not habits:
        st.info("Add habits to start tracking progress.")
    else:
        week_start = (date.today() - timedelta(days=6)).isoformat()
        today = date.today().isoformat()

        with get_connection() as connection:
            weekly_done = connection.execute(
                """
                SELECT COUNT(*)
                FROM completions
                WHERE completed = 1 AND completion_date BETWEEN ? AND ?
                """,
                (week_start, today),
            ).fetchone()[0]

        possible = len(habits) * 7
        rate = round((weekly_done / possible) * 100) if possible else 0

        st.metric("Completions in the last 7 days", weekly_done)
        st.metric("Weekly completion rate", f"{rate}%")

        st.subheader("Habit totals")
        with get_connection() as connection:
            totals = connection.execute(
                """
                SELECT habits.name, COUNT(completions.completion_date)
                FROM habits
                LEFT JOIN completions
                    ON habits.id = completions.habit_id
                    AND completions.completed = 1
                GROUP BY habits.id, habits.name
                ORDER BY habits.name
                """
            ).fetchall()

        for name, count in totals:
            st.write(f"**{name}:** {count} completed")