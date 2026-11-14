
"""
GeoCiment - Generador de plantilla Word.
Ejecutar una sola vez para crear memoria.docx.
"""

from pathlib import Path
from io import BytesIO

import matplotlib.pyplot as plt
import math2docx
from docx import Document
from docx.shared import Cm, Pt


def agregar_ecuacion(documento, formula):
    """
    Inserta una ecuación LaTeX como ecuación nativa
    y editable de Microsoft Word.
    """

    parrafo = documento.add_paragraph()
    parrafo.alignment = 1

    # Convertir LaTeX a ecuación editable.
    math2docx.add_math(parrafo, formula)

    # Separación respecto al texto.
    parrafo.paragraph_format.space_before = Pt(4)
    parrafo.paragraph_format.space_after = Pt(6)

def crear_plantilla():
    raiz = Path(__file__).resolve().parent
    carpeta = raiz / "plantillas"
    carpeta.mkdir(exist_ok=True)

    documento = Document()

    seccion = documento.sections[0]
    seccion.top_margin = Cm(2)
    seccion.bottom_margin = Cm(2)
    seccion.left_margin = Cm(2.5)
    seccion.right_margin = Cm(2.5)

    estilo = documento.styles["Normal"]
    estilo.font.name = "Arial"
    estilo.font.size = Pt(10)

    titulo = documento.add_heading(
        "MEMORIA DE CÁLCULO GEOTÉCNICO", 0
    )
    titulo.alignment = 1

    p = documento.add_paragraph()
    p.alignment = 1
    p.add_run(
        "UNIVERSIDAD DISTRITAL FRANCISCO JOSÉ DE CALDAS\n"
        "FACULTAD TECNOLÓGICA - INGENIERÍA CIVIL\n"
        "PROGRAMACIÓN II - GEOCIMENT"
    ).bold = True

    documento.add_heading(
        "1. IDENTIFICACIÓN DEL PROYECTO", 1
    )
    documento.add_paragraph("Proyecto: {{ proyecto }}")
    documento.add_paragraph("Ubicación: {{ ubicacion }}")
    documento.add_paragraph("Fecha: {{ fecha }}")

    documento.add_heading(
        "2. OBJETIVO Y ALCANCE", 1
    )
    documento.add_paragraph(
        "Evaluar la capacidad portante de una cimentación "
        "superficial mediante el método clásico de Terzaghi, "
        "considerando un suelo homogéneo, una carga vertical "
        "centrada y condiciones idealizadas de falla general."
    )

    documento.add_heading(
        "3. DATOS DE ENTRADA", 1
    )

    for texto in [
        "Cohesión: {{ c }} kPa",
        "Ángulo de fricción: {{ phi }} grados",
        "Peso unitario: {{ gamma }} kN/m³",
        "Ancho B: {{ b }} m",
        "Largo L: {{ l }} m",
        "Profundidad Df: {{ df }} m",
        "Carga vertical P: {{ carga }} kN",
        "Factor de seguridad requerido: {{ fs }}",
    ]:
        documento.add_paragraph(texto)

    documento.add_heading(
        "4. METODOLOGÍA DE CÁLCULO", 1
    )

    documento.add_paragraph(
        "La capacidad portante última se determina mediante "
        "la formulación clásica de Terzaghi, considerando "
        "los factores de forma correspondientes a una "
        "cimentación rectangular."
    )

    documento.add_heading(
        "4.1. Capacidad portante última", 2
    )

    agregar_ecuacion(
        documento,
        r"q_{ult}=cN_c\left(1+0.3\frac{B}{L}\right)"
        r"+\gamma D_fN_q"
        r"+\frac{1}{2}\gamma BN_{\gamma}"
        r"\left(1-0.2\frac{B}{L}\right)"
    )

    documento.add_paragraph(
        "Donde: c es la cohesión del suelo (kPa); "
        "Nc, Nq y Nγ son factores de capacidad portante; "
        "γ es el peso unitario (kN/m³); "
        "Df es la profundidad de desplante (m); "
        "B y L son las dimensiones de la zapata (m)."
    )

    documento.add_heading(
        "4.2. Capacidad portante admisible", 2
    )

    agregar_ecuacion(
        documento,
        r"q_{adm}=\frac{q_{ult}}{FS_{req}}"
    )

    documento.add_paragraph(
        "La capacidad admisible se obtiene dividiendo "
        "la capacidad última entre el factor de seguridad "
        "requerido para el análisis."
    )

    documento.add_heading(
        "4.3. Presión aplicada", 2
    )

    agregar_ecuacion(
        documento,
        r"q_{aplicada}=\frac{P}{B\cdot L}"
    )

    documento.add_paragraph(
        "La presión aplicada corresponde a la carga "
        "vertical de servicio dividida entre el área "
        "de contacto de la cimentación."
    )

    documento.add_heading(
        "4.4. Factor de seguridad disponible", 2
    )

    agregar_ecuacion(
        documento,
        r"FS_{disp}=\frac{q_{ult}}{q_{aplicada}}"
    )

    documento.add_paragraph(
        "Se considera que la cimentación satisface "
        "la verificación de capacidad portante cuando "
        "el factor de seguridad disponible es mayor "
        "o igual al factor requerido."
    )

    documento.add_heading(
        "4.5. Dimensionamiento numérico con SciPy", 2
    )

    agregar_ecuacion(
        documento,
        r"f(B)=q_{adm}(B)-\frac{P}{B^2}=0"
    )

    documento.add_paragraph(
        "El ancho mínimo de una zapata cuadrada se "
        "determina mediante scipy.optimize.brentq. "
        "Este procedimiento busca numéricamente "
        "el valor de B para el cual la capacidad "
        "admisible iguala la presión aplicada, "
        "dentro del intervalo de búsqueda definido."
    )
        

    documento.add_heading(
        "5. RESULTADOS", 1
    )

    tabla = documento.add_table(
        rows=4, cols=2
    )
    tabla.style = "Table Grid"
    tabla.cell(0, 0).text = "Parámetro"
    tabla.cell(0, 1).text = "Resultado"

    # docxtpl repite la fila intermedia usando Jinja.
    tabla.cell(1, 0).text = "{%tr for fila in filas %}"
    tabla.cell(2, 0).text = "{{ fila.concepto }}"
    tabla.cell(2, 1).text = "{{ fila.valor }}"
    tabla.cell(3, 0).text = "{%tr endfor %}"

    documento.add_heading(
        "6. ANÁLISIS GRÁFICO", 1
    )
    documento.add_paragraph("{{ grafica }}")

    documento.add_heading(
        "7. CONCLUSIONES", 1
    )
    documento.add_paragraph("{{ conclusion }}")
    documento.add_paragraph(
        "Los resultados corresponden exclusivamente a "
        "una verificación académica de capacidad portante. "
        "No incluyen el análisis de asentamientos, el efecto "
        "del nivel freático cercano, cargas excéntricas, "
        "estratificación ni otras verificaciones de diseño."
    )

    documento.add_heading(
        "8. REFERENCIA TÉCNICA", 1
    )
    documento.add_paragraph(
        "Terzaghi, K. (1943). Theoretical Soil Mechanics. "
        "John Wiley & Sons. Formulación clásica de capacidad "
        "portante y factores asociados."
    )

    destino = carpeta / "memoria.docx"
    documento.save(destino)

    print(f"Plantilla creada: {destino}")


if __name__ == "__main__":
    crear_plantilla()
