import sqlite3
import hashlib

# ======================================
# CREAR DB SI NO EXISTE
# ======================================
def create_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        name TEXT PRIMARY KEY,
        password TEXT
    )
    """)
    conn.commit()
    conn.close()

# ======================================
# REGISTRAR USUARIO
# ======================================
def register_user(name, password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (name, hashed))
        conn.commit()
        print(f"✅ Usuario '{name}' registrado exitosamente.")
    except sqlite3.IntegrityError:
        print("⚠️ El usuario ya existe.")
    conn.close()

# ======================================
# LOGIN DE USUARIO
# ======================================
def login_user(name, password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name=? AND password=?", (name, hashed))
    user = c.fetchone()
    conn.close()
    if user:
        print(f"✅ Login exitoso para {name}.")
    else:
        print("⚠️ Login fallido. Nombre o contraseña incorrectos.")

# ======================================
# PROGRAMA PRINCIPAL
# ======================================
create_db()

while True:
    print("\n==== MENÚ ====")
    print("1. Registrar usuario")
    print("2. Login")
    print("q. Salir")
    opcion = input("Seleccione una opción: ").lower()

    if opcion == "1":
        name = input("Ingrese nombre de usuario: ")
        password = input("Ingrese contraseña: ")
        register_user(name, password)
    elif opcion == "2":
        name = input("Ingrese nombre de usuario: ")
        password = input("Ingrese contraseña: ")
        login_user(name, password)
    elif opcion in ["q", "quit"]:
        print("🚪 Saliendo del programa.")
        break
    else:
        print("⚠️ Opción no válida.")

input("\nPresiona Enter para cerrar...")
