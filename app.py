from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "clave_super_secreta"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'database.db')

# =========================
# HOME
# =========================
@app.route('/')
def home():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()

    productos_colores = []

    for p in productos:
        min_compradores = p[4] if p[4] else 1
        compradores_actual = p[5] if p[5] else 0

        progreso = min(100, int((compradores_actual / min_compradores) * 100))

        if progreso < 50:
            color = '#f44336'
        elif progreso < 100:
            color = '#ffeb3b'
        else:
            color = '#4caf50'

        productos_colores.append(p + (progreso, color))

    return render_template('index.html', productos=productos_colores)

# =========================
# REGISTER
# =========================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = generate_password_hash(request.form['password'])

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(
                'INSERT INTO usuarios (nombre, password) VALUES (?, ?)',
                (nombre, password)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('register.html', error="Usuario ya existe")

    return render_template('register.html')

# =========================
# LOGIN
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, password FROM usuarios WHERE nombre = ?',
            (nombre,)
        )
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session['usuario_id'] = user[0]
            session['usuario_nombre'] = nombre
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Datos incorrectos")

    return render_template('login.html')

# =========================
# LOGOUT
# =========================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# =========================
# UNIRSE AL GRUPO
# =========================
@app.route('/unirse/<int:producto_id>')
def unirse(producto_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    usuario = session['usuario_nombre']

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        'SELECT stock, compradores_actual FROM productos WHERE id = ?',
        (producto_id,)
    )
    producto = cursor.fetchone()

    if producto:
        stock, compradores_actual = producto

        if compradores_actual < stock:
            cursor.execute(
                'UPDATE productos SET compradores_actual = compradores_actual + 1 WHERE id = ?',
                (producto_id,)
            )

            # Permite comprar múltiples veces
            cursor.execute(
                'INSERT INTO carrito (producto_id, usuario) VALUES (?, ?)',
                (producto_id, usuario)
            )

    conn.commit()
    conn.close()

    return redirect(url_for('home'))

# =========================
# CARRITO
# =========================
@app.route('/carrito')
def carrito():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    usuario = session['usuario_nombre']

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT p.nombre, p.precio
        FROM carrito c
        JOIN productos p ON c.producto_id = p.id
        WHERE c.usuario = ?
    ''', (usuario,))

    items = cursor.fetchall()
    conn.close()

    return render_template('carrito.html', items=items)

# =========================
# DETALLE PRODUCTO
# =========================
@app.route('/producto/<int:producto_id>')
def detalle_producto(producto_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE id = ?', (producto_id,))
    producto = cursor.fetchone()
    conn.close()

    if not producto:
        return "Producto no encontrado", 404

    min_compradores = producto[4] if producto[4] else 1
    compradores_actual = producto[5] if producto[5] else 0

    progreso = min(100, int((compradores_actual / min_compradores) * 100))

    if progreso < 50:
        color = '#f44336'
    elif progreso < 100:
        color = '#ffeb3b'
    else:
        color = '#4caf50'

    producto = producto + (progreso, color)

    return render_template('producto.html', producto=producto)

# =========================
# RUN
# =========================
if __name__ == '__main__':
    app.run(debug=True)