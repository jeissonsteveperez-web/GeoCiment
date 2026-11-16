
"""
GeoCiment - Gráficas técnicas de capacidad portante.

Visualización de capacidad admisible, presión aplicada
y ancho mínimo calculado mediante SciPy.
"""

from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from scipy.optimize import brentq
from app.modelo import (
    factores_terzaghi,
    dimensionar_zapata,
    capacidad_portante,
)


def grafica_capacidad(c, phi, gamma, b, l, df, carga, fs=3.0):
    """
    Genera una gráfica técnica con escala automática.

    Mantiene constante la relación L/B y muestra
    el ancho mínimo de una zapata cuadrada.
    """

    relacion = l / b

    # Dimensionamiento cuadrado con SciPy.
    def ecuacion_ancho(ancho_prueba):
        largo_prueba = ancho_prueba * relacion

        resultado = capacidad_portante(
            c=c,
            phi=phi,
            gamma=gamma,
            b=ancho_prueba,
            l=largo_prueba,
            df=df,
            carga=carga,
            fs=fs,
        )

        return (
            resultado["qadm"]
            - resultado["qaplicada"]
        )

    limite_inferior = 0.30
    limite_superior = 20.0

    if ecuacion_ancho(limite_inferior) >= 0:
        b_min = limite_inferior

    elif ecuacion_ancho(limite_superior) < 0:
        raise ValueError(
            "No se encontró un ancho que cumpla "
            "dentro del intervalo de búsqueda."
        )

    else:
        b_min = brentq(
            ecuacion_ancho,
            limite_inferior,
            limite_superior,
            xtol=1e-6,
        )
    # Intervalo de visualización centrado en la
    # zona de interés, evitando anchos muy pequeños.
    x_inicio = max(0.30, min(b, b_min) * 0.65)
    x_final = max(b, b_min) * 1.40

    if x_final <= x_inicio:
        x_final = x_inicio + 1.0

    anchos = np.linspace(x_inicio, x_final, 400)
    largos = anchos * relacion

    nc, nq, ng = factores_terzaghi(phi)

    q = gamma * df

    # Capacidad portante última vectorizada.
    qult = (
        c * nc * (1 + 0.3 * anchos / largos)
        + q * nq
        + 0.5 * gamma * anchos * ng
        * (1 - 0.2 * anchos / largos)
    )

    qadm = qult / fs
    qaplicada = carga / (anchos * largos)

    # Configuración de la figura.
    fig, ax = plt.subplots(figsize=(9, 5.5))

    ax.plot(
        anchos,
        qadm,
        color="#15803D",
        linewidth=2.5,
        label="Capacidad admisible",
    )

    ax.plot(
        anchos,
        qaplicada,
        color="#EA580C",
        linewidth=2.5,
        label="Presión aplicada",
    )

    # Ancho que el usuario está evaluando.
    ax.axvline(
        b,
        color="#2563EB",
        linestyle="--",
        linewidth=1.7,
        label=f"Ancho evaluado: {b:.2f} m",
    )

    # Solo marcar la intersección cuando la solución
    # sea una raíz real y no el límite inferior.
    solucion = capacidad_portante(
        c, phi, gamma, b_min, b_min * relacion,
        df, carga, fs
    )

    diferencia = abs(
        solucion["qadm"] - solucion["qaplicada"]
    )

    tolerancia = max(
        1e-5,
        solucion["qadm"] * 1e-5
    )

    if diferencia <= tolerancia:
        ax.scatter(
            [b_min],
            [solucion["qadm"]],
            color="#7C3AED",
            s=75,
            zorder=5,
            label=f"Ancho mínimo: {b_min:.3f} m",
        )

        ax.annotate(
            f"B mínimo = {b_min:.3f} m",
            xy=(b_min, solucion["qadm"]),
            xytext=(12, 25),
            textcoords="offset points",
            fontsize=9,
            color="#6D28D9",
            arrowprops=dict(
                arrowstyle="->",
                color="#7C3AED",
            ),
        )

    else:
        ax.axvline(
            b_min,
            color="#7C3AED",
            linestyle=":",
            label=f"Límite de búsqueda: {b_min:.2f} m",
        )

    # Escala automática basada en la región mostrada.
    ymax = max(
        float(np.max(qadm)),
        float(np.max(qaplicada)),
    ) * 1.15

    ax.set_xlim(x_inicio, x_final)
    ax.set_ylim(0, ymax)

    ax.set_title(
        "GeoCiment - Análisis de capacidad portante",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    ax.set_xlabel("Ancho de cimentación B (m)")
    ax.set_ylabel("Presión (kPa)")

    ax.grid(True, alpha=0.25)
    ax.legend(
        loc="upper right",
        fontsize=8,
    )

    fig.tight_layout()

    return fig


if __name__ == "__main__":

    figura = grafica_capacidad(
        c=20,
        phi=25,
        gamma=16.5,
        b=2,
        l=2,
        df=1.5,
        carga=1437,
        fs=3,
    )

    carpeta = (
        Path(__file__).resolve().parent.parent
        / "salidas"
    )

    carpeta.mkdir(exist_ok=True)

    archivo = carpeta / "grafica_prueba.png"

    figura.savefig(
        archivo,
        dpi=180,
        bbox_inches="tight",
    )

    plt.close(figura)

    print(f"Gráfica generada: {archivo}")
