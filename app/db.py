
"""
GeoCiment - Base de datos SQLite.

Almacena proyectos y cálculos geotécnicos.
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime


BASE_DATOS = (
    Path(__file__).resolve().parent.parent
    / "geociment.db"
)


def conectar():
    """Crea una conexión con SQLite."""
    conexion = sqlite3.connect(BASE_DATOS)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def inicializar_db():
    """Crea las tablas automáticamente si no existen."""

    with conectar() as conexion:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS proyectos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                ubicacion TEXT,
                fecha TEXT NOT NULL
            )
        """)

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS calculos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proyecto_id INTEGER NOT NULL,
                entradas TEXT NOT NULL,
                resultados TEXT NOT NULL,
                fecha TEXT NOT NULL,
                FOREIGN KEY (proyecto_id)
                    REFERENCES proyectos(id)
                    ON DELETE CASCADE
            )
        """)


def guardar_proyecto(nombre, ubicacion, entradas, resultados):
    """Guarda un proyecto y su cálculo asociado."""

    if not nombre.strip():
        raise ValueError("El proyecto debe tener un nombre.")

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with conectar() as conexion:
        cursor = conexion.execute(
            """
            INSERT INTO proyectos (nombre, ubicacion, fecha)
            VALUES (?, ?, ?)
            """,
            (nombre.strip(), ubicacion.strip(), fecha),
        )

        proyecto_id = cursor.lastrowid

        conexion.execute(
            """
            INSERT INTO calculos
            (proyecto_id, entradas, resultados, fecha)
            VALUES (?, ?, ?, ?)
            """,
            (
                proyecto_id,
                json.dumps(entradas),
                json.dumps(resultados),
                fecha,
            ),
        )

    return proyecto_id


def listar_proyectos(busqueda=""):
    """Lista proyectos y permite buscar por nombre."""

    with conectar() as conexion:
        registros = conexion.execute(
            """
            SELECT id, nombre, ubicacion, fecha
            FROM proyectos
            WHERE nombre LIKE ?
            ORDER BY id DESC
            """,
            (f"%{busqueda}%",),
        ).fetchall()

    return [dict(fila) for fila in registros]


def obtener_proyecto(proyecto_id):
    """Recupera un proyecto con sus cálculos."""

    with conectar() as conexion:
        proyecto = conexion.execute(
            """
            SELECT * FROM proyectos WHERE id = ?
            """,
            (proyecto_id,),
        ).fetchone()

        if proyecto is None:
            return None

        calculos = conexion.execute(
            """
            SELECT * FROM calculos
            WHERE proyecto_id = ?
            ORDER BY id
            """,
            (proyecto_id,),
        ).fetchall()

    datos = dict(proyecto)

    datos["calculos"] = []

    for calculo in calculos:
        registro = dict(calculo)
        registro["entradas"] = json.loads(
            registro["entradas"]
        )
        registro["resultados"] = json.loads(
            registro["resultados"]
        )
        datos["calculos"].append(registro)

    return datos


def eliminar_proyecto(proyecto_id):
    """Elimina un proyecto y sus cálculos asociados."""

    with conectar() as conexion:
        cursor = conexion.execute(
            """
            DELETE FROM proyectos WHERE id = ?
            """,
            (proyecto_id,),
        )

    return cursor.rowcount > 0


if __name__ == "__main__":
    inicializar_db()
    print("Base de datos GeoCiment creada correctamente.")
