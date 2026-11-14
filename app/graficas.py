
"""
GeoCiment - Gráficas técnicas
Visualización de la capacidad portante.
"""

from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from app.modelo import factores_terzaghi


def grafica_capacidad(c, phi, gamma, b, l, df, carga, fs=3.0):
    """
    Grafica la capacidad admisible y la presión aplicada
    al variar el ancho de una zapata.

    Mantiene constante la relación L/B.
    """

    relacion = l / b

    # Malla de 300 dimensiones evaluadas con NumPy.
    anchos = np.linspace(0.30, max(5.0, b * 2), 300)
    largos = anchos * relacion

    nc, nq, ng = factores_terzaghi(phi)

    q = gamma * df

    qult = (
        c * nc * (1 + 0.3 * anchos / largos)
        + q * nq
        + 0.5 * gamma * anchos * ng
        * (1 - 0.2 * anchos / largos)
    )

    qadm = qult / fs
    qaplicada = carga / (anchos * largos)

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(
        anchos, qadm,
        label="Capacidad admisible",
        color="#147D64",
        linewidth=2.5
    )

    ax.plot(
        anchos, qaplicada,
        label="Presión aplicada",
        color="#D65B45",
        linewidth=2.5
    )

    ax.axvline(
        b,
        color="#3268AB",
        linestyle="--",
        label=f"Ancho evaluado: {b:.2f} m"
    )

    ax.set_title("GeoCiment - Análisis de capacidad portante")
    ax.set_xlabel("Ancho de cimentación B (m)")
    ax.set_ylabel("Presión (kPa)")

    ax.grid(True, alpha=0.25)
    ax.legend()
    ax.set_ylim(bottom=0)

    fig.tight_layout()

    return fig


if __name__ == "__main__":

    figura = grafica_capacidad(
        c=10,
        phi=30,
        gamma=18,
        b=2,
        l=2,
        df=1.5,
        carga=600,
        fs=3
    )

    carpeta = Path(__file__).resolve().parent.parent / "salidas"
    carpeta.mkdir(exist_ok=True)

    archivo = carpeta / "grafica_prueba.png"

    figura.savefig(archivo, dpi=180)
    plt.close(figura)

    print(f"Gráfica generada correctamente: {archivo}")

