from flask import Flask, request, redirect, jsonify, render_template
import sqlite3
import string
import random
import os

app = Flask(__name__)

DB_NAME = "database.db"
SHORT_CODE_LENGTH = 6
CHARACTERS = string.ascii_letters + string.digits


def init_db():
    """Create the urls table if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            clicks INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def generate_short_code(length=SHORT_CODE_LENGTH):
    """Generate a random short code and make sure it's unique."""
    conn = get_db_connection()
    cursor = conn.cursor()
    while True:
        code = ''.join(random.choices(CHARACTERS, k=length))
        cursor.execute("SELECT id FROM urls WHERE short_code = ?", (code,))
        if cursor.fetchone() is None:
            conn.close()
            return code


def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")


@app.route("/")
def home():
    """Basic frontend to input long URLs and see the shortened version."""
    return render_template("index.html")


@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    """
    Accepts a long URL and returns a unique short code.
    Expects JSON body: { "url": "https://example.com/very/long/link" }
    """
    data = request.get_json(silent=True) or request.form

    original_url = data.get("url", "").strip()

    if not original_url:
        return jsonify({"error": "Missing 'url' field"}), 400

    if not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL. Must start with http:// or https://"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # If this URL was already shortened before, return the existing code
    cursor.execute("SELECT short_code FROM urls WHERE original_url = ?", (original_url,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        short_code = existing["short_code"]
    else:
        short_code = generate_short_code()
        cursor.execute(
            "INSERT INTO urls (short_code, original_url) VALUES (?, ?)",
            (short_code, original_url)
        )
        conn.commit()
        conn.close()

    short_url = request.host_url + short_code

    return jsonify({
        "original_url": original_url,
        "short_code": short_code,
        "short_url": short_url
    }), 201


@app.route("/<short_code>")
def redirect_to_original(short_code):
    """Redirect route: visiting the short URL sends the user to the original long URL."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT original_url FROM urls WHERE short_code = ?", (short_code,))
    result = cursor.fetchone()

    if result is None:
        conn.close()
        return jsonify({"error": "Short URL not found"}), 404

    cursor.execute(
        "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?", (short_code,)
    )
    conn.commit()
    conn.close()

    return redirect(result["original_url"])


@app.route("/api/stats/<short_code>")
def get_stats(short_code):
    """Extra endpoint: view click stats for a given short code."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT short_code, original_url, created_at, clicks FROM urls WHERE short_code = ?",
        (short_code,)
    )
    result = cursor.fetchone()
    conn.close()

    if result is None:
        return jsonify({"error": "Short URL not found"}), 404

    return jsonify(dict(result))


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
