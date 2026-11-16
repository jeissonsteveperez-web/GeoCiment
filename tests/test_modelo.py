
"""
GeoCiment - Pruebas del modelo geotécnico.
Universidad Distrital - Programación II.

Pruebas de validación manual, cálculo de capacidad
portante y dimensionamiento con SciPy.
"""

import pytest

from app.modelo import (
    factores_terzaghi,
    capacidad_portante,
    dimensionar_zapata,
)


def test_factores_suelo_cohesivo():
    """Verifica los factores para phi = 0 grados."""

    nc, nq, ng = factores_terzaghi(0)

    assert nc == pytest.approx(5.7)
    assert nq == pytest.approx(1.0)
    assert ng == pytest.approx(0.0)


def test_capacidad_portante_manual():
    """
    Caso resuelto manualmente:
    phi=0, c=10 kPa, gamma=18 kN/m3.
    Zapata de 2 x 2 m a 1.5 m de profundidad.
    """

    r = capacidad_portante(
        c=10,
        phi=0,
        gamma=18,
        b=2,
        l=2,
        df=1.5,
        carga=600,
        fs=3,
    )

    # Resultados obtenidos manualmente.
    assert r["qult"] == pytest.approx(101.10)
    assert r["qadm"] == pytest.approx(33.70)
    assert r["qaplicada"] == pytest.approx(150.0)
    assert r["fs_disponible"] == pytest.approx(0.674)
    assert r["cumple"] is False


def test_suelo_friccionante():
    """
    Verifica el término asociado a N_gamma
    para c=0, Df=0 y phi=30 grados.
    """

    r = capacidad_portante(
        c=0,
        phi=30,
        gamma=18,
        b=2,
        l=2,
        df=0,
        carga=600,
        fs=3,
    )

    # Cálculo manual con N_gamma=19.7:
    # qult = 0.5 * 18 * 2 * 19.7 * 0.8
     # Cálculo manual con N_gamma = 19.13
    # qult = 0.5 * 18 * 2 * 19.13 * 0.8
    # qult = 275.472 kPa

    assert r["qult"] == pytest.approx(275.472)
    assert r["qadm"] == pytest.approx(91.824)
    assert r["qaplicada"] == pytest.approx(150.0)
    assert r["cumple"] is False
    assert r["qaplicada"] == pytest.approx(150.0)
    assert r["cumple"] is False


def test_dimensionamiento_scipy():
    """
    Verifica que SciPy encuentre B=2.00 m
    en un caso de solución conocida.
    """

    b = dimensionar_zapata(
        c=100,
        phi=0,
        gamma=18,
        df=0,
        carga=988,
        fs=3,
    )

    assert b == pytest.approx(2.0, abs=0.001)


def test_datos_invalidos():
    """Comprueba que se rechacen dimensiones negativas."""

    with pytest.raises(ValueError):
        capacidad_portante(
            c=10,
            phi=30,
            gamma=18,
            b=-2,
            l=2,
            df=1.5,
            carga=600,
            fs=3,
        )

def test_ejemplo_16_1_libro():
    """
    Validación con el ejemplo 16.1 del libro.

    Zapata cuadrada de 2 x 2 m.
    c = 20 kPa
    phi = 25 grados
    gamma = 16.5 kN/m3
    Df = 1.5 m
    FS = 3
    """

    r = capacidad_portante(
        c=20,
        phi=25,
        gamma=16.5,
        b=2,
        l=2,
        df=1.5,
        carga=1438,
        fs=3,
    )

    assert r["Nc"] == pytest.approx(25.13)
    assert r["Nq"] == pytest.approx(12.72)
    assert r["Ngamma"] == pytest.approx(8.34)

    assert r["qult"] == pytest.approx(
        1078.288, abs=0.01
    )

    assert r["qadm"] == pytest.approx(
        359.4293, abs=0.01
    )

    # Carga admisible total en kN.
    carga_admisible = r["qadm"] * 2 * 2

    assert carga_admisible == pytest.approx(
        1437.7173, abs=0.05
    )
def test_carga_admisible_total():
    """Comprueba la carga admisible del ejemplo 16.1."""

    r = capacidad_portante(
        c=20,
        phi=25,
        gamma=16.5,
        b=2,
        l=2,
        df=1.5,
        carga=1438,
        fs=3,
    )

    assert r["Qadm"] == pytest.approx(
        1437.7173, abs=0.05
    )