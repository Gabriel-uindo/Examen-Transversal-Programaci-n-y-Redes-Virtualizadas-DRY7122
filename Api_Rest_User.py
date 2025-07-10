from flask import Flask, request, jsonify
import sqlite3
import hashlib

app = Flask(__name__)

# ==========================================
# FUNCIONES DE BASE DE DATOS
# ==========================================

def init_db():
    """Crea la base de datos si no existe"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        name TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def add_user(name, password_hash):
    """Agrega un usuario a la base de datos"""
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(name, password_hash):
    """Verifica si existe el usuario con la contraseña hash"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name=? AND password=?", (name, password_hash))
    result = c.fetchone()
    conn.close()
    return result is not None

# ==========================================
# RUTAS API
# ==========================================

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    password = request.form.get('password')
    
    if not name or not password:
        return jsonify({"status": "error", "message": "Faltan parámetros 'name' o 'password'"}), 400
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if add_user(name, password_hash):
        return jsonify({"status": "success", "message": f"Usuario {name} registrado exitosamente."}), 201
    else:
        return jsonify({"status": "error", "message": "El usuario ya existe."}), 409

@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('password')
    
    if not name or not password:
        return jsonify({"status": "error", "message": "Faltan parámetros 'name' o 'password'"}), 400
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if verify_user(name, password_hash):
        return jsonify({"status": "success", "message": f"Login exitoso. Bienvenido {name}"}), 200
    else:
        return jsonify({"status": "error", "message": "Login fallido. Usuario o contraseña incorrectos."}), 401

# ==========================================
# INICIO DEL SERVIDOR
# ==========================================

if __name__ == '__main__':
    init_db()
    print("✅ Base de datos inicializada.")
    app.run(host='0.0.0.0', port=5800, debug=True)

