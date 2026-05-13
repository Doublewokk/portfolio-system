from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(name)

# =========================================
# DATABASE
# =========================================

conn = sqlite3.connect(
    "portfolio.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

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

# =========================================
# HOME
# =========================================

@app.route("/")
def home():

    return render_template("index.html")

# =========================================
# SAVE PORTFOLIO
# =========================================

@app.route("/save", methods=["POST"])
def save():

    data = request.json

    cursor.execute("""

    INSERT INTO users (

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
        "message":"saved"
    })

# =========================================
# GET USERS
# =========================================

@app.route("/users")
def users():

    cursor.execute("""

    SELECT
        id,
        name,
        skills,
        github,
        category,
        contacts,
        views,
        photo

    FROM users

    """)

    users = cursor.fetchall()

    result = []

    for user in users:

        result.append({

            "id":user[0],
            "name":user[1],
            "skills":user[2],
            "github":user[3],
            "category":user[4],
            "contacts":user[5],
            "views":user[6],
            "photo":user[7]

        })

    return jsonify(result)

# =========================================
# SEARCH USERS
# =========================================

@app.route("/search/<query>")
def search(query):

    cursor.execute("""

    SELECT
        name,
        skills,
        github,
        category,
        contacts,
        photo

    FROM users

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

    users = cursor.fetchall()

    result = []

    for user in users:

        result.append({

            "name":user[0],
            "skills":user[1],
            "github":user[2],
            "category":user[3],
            "contacts":user[4],
            "photo":user[5]

        })

    return jsonify(result)

# =========================================
# STATS
# =========================================

@app.route("/stats")
def stats():

    cursor.execute("""
    SELECT COUNT(*)
    FROM users
    """)

    users_count = cursor.fetchone()[0]

    cursor.execute("""
    SELECT SUM(views)
    FROM users
    """)

    views = cursor.fetchone()[0]

    if views is None:
        views = 0

    return jsonify({

        "users":users_count,
        "views":views,
        "active":users_count

    })

# =========================================
# RUN
# =========================================

if name == "main":
    app.run(host="0.0.0.0", port=5000)
