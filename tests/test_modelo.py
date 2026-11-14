
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
    assert r["qult"] == pytest.approx(283.68)
    assert r["qadm"] == pytest.approx(94.56)
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
