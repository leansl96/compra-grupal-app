import sqlite3
import os
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'database.db')

# ⚠️ Solo para desarrollo: borra la DB cada vez
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# =========================
# TABLA PRODUCTOS
# =========================
cursor.execute('''
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL,
    min_compradores INTEGER NOT NULL,
    compradores_actual INTEGER DEFAULT 0,
    descripcion TEXT,
    imagen TEXT
)
''')

# Productos de ejemplo
productos = [
    ("Auriculares Inalámbricos", 2500.0, 50, 5, "Auriculares bluetooth con cancelación de ruido, 20h batería.", "auriculares.jpg"),
    ("Smartwatch Deportivo", 7500.0, 30, 3, "Smartwatch resistente al agua con monitor cardíaco.", "smartwatch.jpg"),
    ("Teclado Mecánico", 9800.0, 20, 4, "Teclado mecánico RGB con switches azules.", "teclado.jpg"),
    ("Mouse Gamer RGB", 3500.0, 40, 6, "Mouse ergonómico con alta precisión.", "mouse.jpg")
]

cursor.executemany('''
INSERT INTO productos (nombre, precio, stock, min_compradores, descripcion, imagen)
VALUES (?, ?, ?, ?, ?, ?)
''', productos)

# =========================
# TABLA CARRITO
# =========================
cursor.execute('''
CREATE TABLE carrito (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,
    usuario TEXT NOT NULL,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
)
''')

# =========================
# TABLA USUARIOS
# =========================
cursor.execute('''
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Usuario demo
cursor.execute(
    'INSERT INTO usuarios (nombre, password) VALUES (?, ?)',
    ("demo", generate_password_hash("1234"))
)

conn.commit()
conn.close()

print("✅ Base de datos creada correctamente")