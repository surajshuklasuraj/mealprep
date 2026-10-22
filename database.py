"""
database.py
Local SQLite storage for saved recipes.
Uses the standard library sqlite3 — no extra dependencies.
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = "mealprep.db"


def _get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            url TEXT,
            title TEXT,
            original_servings INTEGER,
            scaled_servings INTEGER,
            ingredients_json TEXT,
            saved_at TEXT
        )
    """)
    conn.commit()


def save_recipe(name, url, recipe, scaled_servings, scaled_ingredients):
    """Save or replace a recipe in the local database."""
    conn = _get_connection()
    _init_db(conn)
    conn.execute("""
        INSERT OR REPLACE INTO recipes
            (name, url, title, original_servings, scaled_servings, ingredients_json, saved_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        url,
        recipe.get('title', ''),
        recipe.get('servings', 4),
        scaled_servings,
        json.dumps(scaled_ingredients),
        datetime.now().strftime("%Y-%m-%d %H:%M"),
    ))
    conn.commit()
    conn.close()


def list_saved_recipes():
    """Return a list of all saved recipe names and dates."""
    conn = _get_connection()
    _init_db(conn)
    rows = conn.execute("SELECT name, saved_at FROM recipes ORDER BY saved_at DESC").fetchall()
    conn.close()
    return [{'name': r['name'], 'saved_at': r['saved_at']} for r in rows]


def get_saved_recipe(name):
    """Return the full data for one saved recipe by name, or None if not found."""
    conn = _get_connection()
    _init_db(conn)
    row = conn.execute("SELECT * FROM recipes WHERE name = ?", (name,)).fetchone()
    conn.close()
    if not row:
        return None
    return {
        'name': row['name'],
        'url': row['url'],
        'title': row['title'],
        'original_servings': row['original_servings'],
        'scaled_servings': row['scaled_servings'],
        'ingredients': json.loads(row['ingredients_json']),
        'saved_at': row['saved_at'],
    }
