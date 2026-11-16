
"""
GeoCiment - Generación de memoria de cálculo en Word.
Utiliza docxtpl y las gráficas de Matplotlib.
"""

from pathlib import Path
from datetime import datetime
from io import BytesIO

import matplotlib.pyplot as plt
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

from app.db import obtener_proyecto, listar_proyectos
from app.graficas import grafica_capacidad


RAIZ = Path(__file__).resolve().parent.parent
PLANTILLA = RAIZ / "plantillas" / "memoria.docx"
REPORTES = RAIZ / "salidas" / "reportes"


def generar_memoria(proyecto_id):
    """
    Genera la memoria Word de un proyecto guardado.

    Retorna la ruta del documento generado.
    """

    proyecto = obtener_proyecto(proyecto_id)

    if proyecto is None:
        raise ValueError("El proyecto no existe.")

    if not proyecto["calculos"]:
        raise ValueError(
            "El proyecto no contiene cálculos guardados."
        )

    if not PLANTILLA.exists():
        raise FileNotFoundError(
            "No existe plantillas/memoria.docx. "
            "Ejecuta primero crear_plantilla.py."
        )

    # Recuperar el cálculo más reciente.
    calculo = proyecto["calculos"][-1]

    datos = calculo["entradas"]
    r = calculo["resultados"]

    c = datos["c"]
    phi = datos["phi"]
    gamma = datos["gamma"]
    b = datos["b"]
    l = datos["l"]
    df = datos["df"]
    carga = datos["carga"]
    fs = datos["fs"]

    # Generar la misma gráfica utilizada en la app.
    figura = grafica_capacidad(
        c, phi, gamma, b, l, df, carga, fs
    )

    imagen = BytesIO()

    try:
        figura.savefig(
            imagen,
            format="png",
            dpi=160,
            bbox_inches="tight",
        )
    finally:
        plt.close(figura)

    imagen.seek(0)

    # Abrir plantilla docxtpl.
    documento = DocxTemplate(PLANTILLA)

    filas = [
        {
            "concepto": "Factor Nc",
            "valor": f"{r['Nc']:.3f}",
        },
        {
            "concepto": "Factor Nq",
            "valor": f"{r['Nq']:.3f}",
        },
        {
            "concepto": "Factor Nγ",
            "valor": f"{r['Ngamma']:.3f}",
        },
        {
            "concepto": "Capacidad última",
            "valor": f"{r['qult']:.3f} kPa",
        },
        {
            "concepto": "Capacidad admisible",
            "valor": f"{r['qadm']:.3f} kPa",
        },
        {
            "concepto": "Carga admisible total",
            "valor": f"{r['Qadm']:.3f} kN",
        },
        {
            "concepto": "Presión aplicada",
            "valor": f"{r['qaplicada']:.3f} kPa",
        },
        {
            "concepto": "FS requerido",
            "valor": f"{fs:.3f}",
        },
        {
            "concepto": "FS disponible",
            "valor": f"{r['fs_disponible']:.3f}",
        },
        {
            "concepto": "Ancho mínimo cuadrado",
            "valor": f"{r['ancho_minimo']:.3f} m",
        },
        {
            "concepto": "Área mínima cuadrada",
            "valor": f"{r['area_minima']:.3f} m²",
        },
    ]

    if r["cumple"]:
        conclusion = (
            "La presión aplicada es menor o igual "
            "a la capacidad portante admisible. "
            "Por tanto, la cimentación evaluada CUMPLE "
            "la verificación de capacidad portante "
            "bajo las hipótesis adoptadas."
        )
    else:
        conclusion = (
            "La presión aplicada supera la capacidad "
            "portante admisible. Por tanto, la cimentación "
            "NO CUMPLE la verificación de capacidad "
            "portante bajo las hipótesis adoptadas."
        )

    contexto = {
        "proyecto": proyecto["nombre"],
        "ubicacion": proyecto["ubicacion"] or "No indicada",
        "fecha": calculo["fecha"],
        "c": f"{c:.3f}",
        "phi": f"{phi:.3f}",
        "gamma": f"{gamma:.3f}",
        "b": f"{b:.3f}",
        "l": f"{l:.3f}",
        "df": f"{df:.3f}",
        "carga": f"{carga:.3f}",
        "fs": f"{fs:.3f}",
        "filas": filas,
        "grafica": InlineImage(
            documento,
            imagen,
            width=Mm(150),
        ),
        "conclusion": conclusion,
    }

    documento.render(contexto)

    REPORTES.mkdir(
        parents=True,
        exist_ok=True,
    )

    fecha_archivo = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    destino = REPORTES / (
        f"Memoria_GeoCiment_{proyecto_id}_"
        f"{fecha_archivo}.docx"
    )

    documento.save(destino)

    return destino


if __name__ == "__main__":
    proyectos = listar_proyectos()

    if not proyectos:
        print(
            "No hay proyectos guardados. "
            "Guarda primero un cálculo desde GeoCiment."
        )
    else:
        proyecto_id = proyectos[0]["id"]

        ruta = generar_memoria(proyecto_id)

        print("MEMORIA GENERADA CORRECTAMENTE")
        print(f"Proyecto ID: {proyecto_id}")
        print(f"Archivo: {ruta}")
