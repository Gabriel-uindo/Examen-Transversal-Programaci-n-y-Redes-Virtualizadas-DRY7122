from flask import Flask, request, jsonify
import sqlite3
import hashlib

app = Flask(__name__)

def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            name TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    password = request.form.get('password')

    if not name or not password:
        return jsonify({"status": "error", "message": "Faltan parámetros"}), 400

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "message": "Usuario ya existe"}), 409
    finally:
        conn.close()

    return jsonify({"status": "success", "message": f"Usuario {name} registrado"}), 201

@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('password')

    if not name or not password:
        return jsonify({"status": "error", "message": "Faltan parámetros"}), 400

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name = ? AND password = ?", (name, hashed_password))
    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({"status": "success", "message": f"Login exitoso para {name}"}), 200
    else:
        return jsonify({"status": "error", "message": "Login fallido"}), 401

if __name__ == '__main__':
    create_db()
    app.run(port=5800, debug=True)

