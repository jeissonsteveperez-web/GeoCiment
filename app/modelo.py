
"""
GeoCiment - Modelo geotécnico
Capacidad portante de cimentaciones superficiales.
Universidad Distrital - Programación II.
"""

import numpy as np
from scipy.optimize import brentq

def factores_terzaghi(phi):
    """Calcula factores de capacidad portante de Terzaghi."""
    if not 0 <= phi < 45:
        raise ValueError("El ángulo phi debe estar entre 0 y 45 grados.")

    if phi == 0:
        return 5.7, 1.0, 0.0

    rad = np.radians(phi)

    nq = (
        np.exp((1.5 * np.pi - rad) * np.tan(rad))
        / (2 * np.cos(np.radians(45) + rad / 2) ** 2)
    )
    nc = (nq - 1) / np.tan(rad)

    # Aproximación tabulada de Terzaghi para N_gamma.
    # Se sustituirá por interpolación de la tabla de referencia.
    tabla_phi = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45])
    tabla_ng = np.array([0, 0.5, 1.2, 2.5, 5.0, 9.7, 19.7, 42.4, 100.4, 297.5])
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
    qaplicada = carga / (b * l)
    fs_disponible = qult / qaplicada

    return {
        "Nc": nc,
        "Nq": nq,
        "Ngamma": ng,
        "qult": qult,
        "qadm": qadm,
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
