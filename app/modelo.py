
"""
GeoCiment - Modelo geotécnico
Capacidad portante de cimentaciones superficiales.
Universidad Distrital - Programación II.
"""

import numpy as np
from scipy.optimize import brentq


def factores_terzaghi(phi):
    """
    Factores de capacidad portante de Terzaghi.

    Fuente: Tabla 16.1 del libro utilizado para
    validar el ejemplo 16.1.

    Para valores intermedios de phi se utiliza
    interpolación lineal mediante NumPy.
    """

    if not np.isfinite(phi) or not 0 <= phi < 45:
        raise ValueError(
            "El ángulo phi debe estar entre 0 y 45 grados "
            "(sin incluir 45)."
        )

    # Ángulos de la tabla, en grados.
    tabla_phi = np.arange(0, 46, dtype=float)

    # Factor Nc
    tabla_nc = np.array([
        5.70, 6.00, 6.30, 6.62, 6.97,
        7.34, 7.73, 8.15, 8.60, 9.09,
        9.61, 10.16, 10.76, 11.41, 12.11,
        12.86, 13.68, 14.60, 15.12, 16.56,
        17.69, 18.92, 20.27, 21.75, 23.36,
        25.13, 27.09, 29.24, 31.61, 34.24,
        37.16, 40.41, 44.04, 48.09, 52.64,
        57.75, 63.53, 70.01, 77.50, 85.97,
        95.66, 106.81, 119.67, 134.58, 151.95,
        172.28
    ])

    # Factor Nq
    tabla_nq = np.array([
        1.00, 1.10, 1.22, 1.35, 1.49,
        1.64, 1.81, 2.00, 2.21, 2.44,
        2.69, 2.98, 3.29, 3.63, 4.02,
        4.45, 4.92, 5.45, 6.04, 6.70,
        7.44, 8.26, 9.19, 10.23, 11.40,
        12.72, 14.21, 15.90, 17.81, 19.98,
        22.46, 25.28, 28.52, 32.23, 36.50,
        41.44, 47.16, 53.80, 61.55, 70.61,
        81.27, 93.85, 108.75, 126.50, 147.74,
        173.28
    ])

    # Factor N_gamma
    tabla_ng = np.array([
        0.00, 0.01, 0.04, 0.06, 0.10,
        0.14, 0.20, 0.27, 0.35, 0.44,
        0.56, 0.69, 0.85, 1.04, 1.26,
        1.52, 1.82, 2.18, 2.59, 3.07,
        3.64, 4.31, 5.09, 6.00, 7.08,
        8.34, 9.84, 11.60, 13.70, 16.18,
        19.13, 22.65, 26.87, 31.94, 38.04,
        45.41, 54.36, 65.27, 78.61, 95.03,
        115.31, 140.51, 171.99, 211.56, 261.60,
        325.34
    ])

    nc = np.interp(phi, tabla_phi, tabla_nc)
    nq = np.interp(phi, tabla_phi, tabla_nq)
    ng = np.interp(phi, tabla_phi, tabla_ng)

    return float(nc), float(nq), float(ng)



def capacidad_portante(c, phi, gamma, b, l, df, carga, fs=3.0):
    """Calcula la capacidad portante y verifica una zapata."""
    if min(gamma, b, l, carga, fs) <= 0:
        raise ValueError("Peso unitario, dimensiones, carga y FS deben ser positivos.")
    if c < 0 or df < 0:
        raise ValueError("La cohesión y la profundidad no pueden ser negativas.")
    if b > l:
        raise ValueError("El ancho B debe ser menor o igual al largo L.")

    nc, nq, ng = factores_terzaghi(phi)
    q = gamma * df

    sc = 1 + 0.3 * b / l
    sg = 1 - 0.2 * b / l

    qult = c * nc * sc + q * nq + 0.5 * gamma * b * ng * sg
    qadm = qult / fs
    q_admisible_total = qadm * b * l
    qaplicada = carga / (b * l)
    fs_disponible = qult / qaplicada

    return {
        "Nc": nc,
        "Nq": nq,
        "Ngamma": ng,
        "qult": qult,
        "qadm": qadm,
        "Qadm": q_admisible_total,
        "qaplicada": qaplicada,
        "fs_disponible": fs_disponible,
        "cumple": qaplicada <= qadm,
    }


def dimensionar_zapata(c, phi, gamma, df, carga, fs=3.0):
    """
    Determina el ancho mínimo de una zapata cuadrada
    mediante el método numérico de Brent (SciPy).

    Se busca que la presión aplicada sea igual
    a la capacidad portante admisible.
    """

    def ecuacion(b):
        resultado = capacidad_portante(
            c=c,
            phi=phi,
            gamma=gamma,
            b=b,
            l=b,
            df=df,
            carga=carga,
            fs=fs
        )

        return resultado["qadm"] - resultado["qaplicada"]

    ancho_minimo = 0.30
    ancho_maximo = 20.0

    if ecuacion(ancho_minimo) >= 0:
        return ancho_minimo

    if ecuacion(ancho_maximo) < 0:
        raise ValueError(
            "No se encontró una solución dentro "
            "del intervalo de búsqueda."
        )

    ancho_calculado = brentq(
        ecuacion,
        ancho_minimo,
        ancho_maximo,
        xtol=1e-6
    )

    return float(ancho_calculado)

if __name__ == "__main__":
    resultado = capacidad_portante(
        c=10,
        phi=30,
        gamma=18,
        b=2,
        l=2,
        df=1.5,
        carga=600,
        fs=3,
    )

    print("\nGEOCIMENT - PRIMER CÁLCULO")
    print("-" * 40)

    for nombre, valor in resultado.items():
        if isinstance(valor, (float, np.floating)):
            print(f"{nombre}: {valor:.3f}")
        else:
            print(f"{nombre}: {valor}")

    print("\nDIMENSIONAMIENTO AUTOMÁTICO")
    print("-" * 40)

    ancho = dimensionar_zapata(
        c=10,
        phi=30,
        gamma=18,
        df=1.5,
        carga=600,
        fs=3
    )

    print(f"Ancho mínimo calculado: {ancho:.3f} m")
    print(f"Área mínima calculada: {ancho**2:.3f} m²")
