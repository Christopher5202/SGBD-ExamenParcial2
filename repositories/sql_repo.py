import sqlite3
import os
from typing import List, Dict, Any

class SQLRepository:
    """
    Repositorio para persistencia transaccional en SQLite.
    """
    def __init__(self, db_path: str = "data/biblioteca.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Inicializa el esquema de la base de datos."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabla Libros
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS libros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    isbn TEXT UNIQUE NOT NULL,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    anio INTEGER,
                    genero TEXT,
                    disponible INTEGER DEFAULT 1,
                    tipo TEXT,
                    formato TEXT,
                    tamano_mb REAL,
                    url_descarga TEXT,
                    ubicacion TEXT,
                    num_ejemplares INTEGER
                )
            ''')
            
            # Tabla Usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    nombre TEXT NOT NULL,
                    contrasena_hash TEXT,
                    libros_prestados INTEGER DEFAULT 0,
                    tipo TEXT,
                    carrera TEXT,
                    semestre INTEGER,
                    departamento TEXT,
                    nivel_acceso INTEGER
                )
            ''')
            
            # Tabla Prestamos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prestamos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_email TEXT NOT NULL,
                    libro_isbn TEXT NOT NULL,
                    fecha_prestamo TEXT NOT NULL,
                    fecha_devolucion TEXT,
                    estado TEXT DEFAULT 'Activo',
                    multa REAL DEFAULT 0.0,
                    FOREIGN KEY(usuario_email) REFERENCES usuarios(email),
                    FOREIGN KEY(libro_isbn) REFERENCES libros(isbn)
                )
            ''')
            
            # Insertar Usuario Admin por defecto para pruebas del profesor
            cursor.execute("INSERT OR IGNORE INTO usuarios (email, nombre, tipo) VALUES ('admin@biblioteca.com', 'Administrador General', 'Bibliotecario')")
            
            conn.commit()

    # ================= LIBROS =================
    def add_libro(self, libro_data: dict):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO libros (isbn, titulo, autor, anio, genero, disponible, tipo, formato, tamano_mb, url_descarga, ubicacion, num_ejemplares)
                VALUES (:isbn, :titulo, :autor, :anio, :genero, :disponible, :tipo, :formato, :tamano_mb, :url_descarga, :ubicacion, :num_ejemplares)
            ''', libro_data)
            conn.commit()

    def get_libros(self) -> List[dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM libros")
            return [dict(row) for row in cursor.fetchall()]

    def update_libro(self, isbn: str, libro_data: dict):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            libro_data['target_isbn'] = isbn
            cursor.execute('''
                UPDATE libros 
                SET titulo=:titulo, autor=:autor, anio=:anio, genero=:genero, disponible=:disponible, 
                    tipo=:tipo, formato=:formato, tamano_mb=:tamano_mb, url_descarga=:url_descarga, 
                    ubicacion=:ubicacion, num_ejemplares=:num_ejemplares
                WHERE isbn=:target_isbn
            ''', libro_data)
            conn.commit()

    def delete_libro(self, isbn: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM libros WHERE isbn=?", (isbn,))
            conn.commit()

    # ================= USUARIOS =================
    def add_usuario(self, usuario_data: dict):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios (email, nombre, contrasena_hash, libros_prestados, tipo, carrera, semestre, departamento, nivel_acceso)
                VALUES (:email, :nombre, :contrasena_hash, :libros_prestados, :tipo, :carrera, :semestre, :departamento, :nivel_acceso)
            ''', usuario_data)
            conn.commit()

    def get_usuarios(self) -> List[dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            return [dict(row) for row in cursor.fetchall()]

    def update_usuario_prestamos(self, email: str, incremento: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE usuarios SET libros_prestados = libros_prestados + ? WHERE email = ?
            ''', (incremento, email))
            conn.commit()

    # ================= PRESTAMOS =================
    def add_prestamo(self, prestamo_data: dict):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO prestamos (usuario_email, libro_isbn, fecha_prestamo, estado)
                VALUES (:usuario_email, :libro_isbn, :fecha_prestamo, :estado)
            ''', prestamo_data)
            conn.commit()
            
    def get_prestamos(self) -> List[dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM prestamos")
            return [dict(row) for row in cursor.fetchall()]

    def devolver_prestamo(self, prestamo_id: int, fecha_devolucion: str, multa: float):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE prestamos 
                SET estado='Devuelto', fecha_devolucion=?, multa=?
                WHERE id=?
            ''', (fecha_devolucion, multa, prestamo_id))
            conn.commit()
