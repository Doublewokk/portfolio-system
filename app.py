from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "database.db"

def connect_db():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    return conn

conn = connect_db()
cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS portfolios(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,
    about TEXT,
    skills TEXT,
    projects TEXT,
    contacts TEXT,
    github TEXT,
    category TEXT,
    education TEXT,
    experience TEXT,
    achievements TEXT,
    photo TEXT,

    views INTEGER DEFAULT 0

)

""")

conn.commit()

@app.route("/")
def home():

    return render_template("index.html")

@app.route("/save", methods=["POST"])
def save():

    data = request.json

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO portfolios(

        name,
        about,
        skills,
        projects,
        contacts,
        github,
        category,
        education,
        experience,
        achievements,
        photo

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        data["name"],
        data["about"],
        data["skills"],
        data["projects"],
        data["contacts"],
        data["github"],
        data["category"],
        data["education"],
        data["experience"],
        data["achievements"],
        data["photo"]

    ))

    conn.commit()

    return jsonify({
        "status":"success"
    })

@app.route("/users")
def users():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM portfolios
    ORDER BY id DESC
    """)

    users = [
        dict(row)
        for row in cursor.fetchall()
    ]

    return jsonify(users)

@app.route("/stats")
def stats():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*) FROM portfolios
    """)

    users = cursor.fetchone()[0]

    cursor.execute("""
    SELECT SUM(views) FROM portfolios
    """)

    views = cursor.fetchone()[0]

    if views is None:
        views = 0

    return jsonify({

        "users":users,
        "views":views,
        "active":users

    })

@app.route("/search/<query>")
def search(query):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT * FROM portfolios

    WHERE

    name LIKE ?
    OR skills LIKE ?
    OR contacts LIKE ?
    OR github LIKE ?
    OR category LIKE ?

    """, (

        f"%{query}%",
        f"%{query}%",
        f"%{query}%",
        f"%{query}%",
        f"%{query}%"

    ))

    users = [
        dict(row)
        for row in cursor.fetchall()
    ]

    return jsonify(users)

if __name__ == "__main__":

    app.run(debug=True)
