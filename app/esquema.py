
"""
GeoCiment - Esquema dinámico de cimentación superficial.

Genera una vista en planta y un corte esquemático
utilizando los parámetros y resultados de GeoCiment.

El espesor de la zapata y la columna son ilustrativos.
No corresponde a un diseño estructural.
"""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch


def generar_esquema(entradas, resultados):
    """
    Genera el esquema de una zapata superficial.

    entradas: diccionario creado en main.py
    resultados: diccionario de capacidad_portante()

    Retorna una figura Matplotlib.
    """

    b = float(entradas["b"])
    l = float(entradas["l"])
    df = float(entradas["df"])
    p = float(entradas["carga"])
    c = float(entradas["c"])
    phi = float(entradas["phi"])
    gamma = float(entradas["gamma"])

    qadm = float(resultados["qadm"])
    qaplicada = float(resultados["qaplicada"])
    qtotal = float(resultados.get("Qadm", qadm * b * l))
    fs_disp = float(resultados["fs_disponible"])
    cumple = bool(resultados["cumple"])

    fig = plt.figure(figsize=(12, 8), facecolor="white")

    fig.suptitle(
        "GEOCIMENT - ESQUEMA DE CIMENTACIÓN SUPERFICIAL",
        fontsize=15,
        fontweight="bold",
        color="#153C70",
        y=0.97,
    )

    # -------------------------------------------------
    # VISTA EN PLANTA
    # -------------------------------------------------

    ax1 = fig.add_axes([0.06, 0.37, 0.40, 0.48])

    ax1.set_title(
        "VISTA EN PLANTA",
        fontsize=12,
        fontweight="bold",
        color="#153C70",
    )

    # Zapata con dimensiones reales B y L.
    zapata_planta = Rectangle(
        (0, 0),
        b,
        l,
        linewidth=1.5,
        edgecolor="#94A3B8",
        facecolor="#F1F5F9",
        hatch=".",
    )

    ax1.add_patch(zapata_planta)

    # Ejes centrales.
    ax1.plot(
        [b / 2, b / 2],
        [-l * 0.08, l * 1.08],
        "--",
        color="#64748B",
        linewidth=1,
    )

    ax1.plot(
        [-b * 0.08, b * 1.08],
        [l / 2, l / 2],
        "--",
        color="#64748B",
        linewidth=1,
    )

    # Cota horizontal B.
    y_cota = -l * 0.18

    ax1.annotate(
        "",
        xy=(0, y_cota),
        xytext=(b, y_cota),
        arrowprops=dict(arrowstyle="<->", color="#153C70"),
    )

    ax1.text(
        b / 2, y_cota - l * 0.045,
        f"B = {b:.2f} m",
        ha="center",
        va="top",
        fontsize=10,
        fontweight="bold",
    )

    # Cota vertical L.
    x_cota = -b * 0.18

    ax1.annotate(
        "",
        xy=(x_cota, 0),
        xytext=(x_cota, l),
        arrowprops=dict(arrowstyle="<->", color="#153C70"),
    )

    ax1.text(
        x_cota - b * 0.045, l / 2,
        f"L = {l:.2f} m",
        rotation=90,
        ha="right",
        va="center",
        fontsize=10,
        fontweight="bold",
    )

    ax1.set_xlim(-b * 0.4, b * 1.3)
    ax1.set_ylim(-l * 0.35, l * 1.2)
    ax1.set_aspect("equal", adjustable="box")
    ax1.axis("off")

    # -------------------------------------------------
    # CORTE ESQUEMÁTICO
    # -------------------------------------------------

    ax2 = fig.add_axes([0.54, 0.37, 0.41, 0.48])

    ax2.set_title(
        "CORTE A-A",
        fontsize=12,
        fontweight="bold",
        color="#153C70",
    )

    # Altura ilustrativa, NO calculada.
    h = max(b * 0.15, 0.15)
    altura_columna = max(df * 0.45, 0.40)

    base = -df
    nivel_terreno = 0

    # Suelo natural.
    fondo = min(base - h * 1.5, -0.6)

    suelo = Rectangle(
        (-b * 0.45, fondo),
        b * 1.9,
        -fondo,
        facecolor="#E8C49C",
        edgecolor="none",
        hatch="///",
        alpha=0.65,
    )
    ax2.add_patch(suelo)

    # Línea de terreno natural.
    ax2.plot(
        [-b * 0.45, b * 1.45],
        [nivel_terreno, nivel_terreno],
        color="#48743B",
        linewidth=2.5,
    )

    # Zapata: base ubicada a profundidad Df.
    zapata_corte = Rectangle(
        (0, base),
        b,
        h,
        facecolor="#F1F5F9",
        edgecolor="#94A3B8",
        linewidth=1.5,
        hatch=".",
        zorder=3,
    )
    ax2.add_patch(zapata_corte)

    # Columna meramente representativa.
    ancho_columna = b * 0.22
    x_columna = (b - ancho_columna) / 2

    columna = Rectangle(
        (x_columna, base + h),
        ancho_columna,
        max(df - h, 0) + altura_columna,
        facecolor="#CBD5E1",
        edgecolor="#1E293B",
        linewidth=1.5,
        zorder=4,
    )
    ax2.add_patch(columna)

    # Carga vertical aplicada.
    tope_columna = (
        base + h + max(df - h, 0) + altura_columna
    )

    ax2.annotate(
        "",
        xy=(b / 2, tope_columna),
        xytext=(b / 2, tope_columna + h * 0.9),
        arrowprops=dict(
            arrowstyle="-|>",
            mutation_scale=23,
            color="#C62828",
            lw=2,
        ),
    )

    ax2.text(
        b / 2,
        tope_columna + h,
        f"P = {p:,.2f} kN",
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold",
        color="#C62828",
    )

    # Cota de profundidad de desplante.
    x_df = -b * 0.22

    if df > 0:
        ax2.annotate(
            "",
            xy=(x_df, 0),
            xytext=(x_df, base),
            arrowprops=dict(
                arrowstyle="<->",
                color="#153C70",
                lw=1.5,
            ),
        )

    ax2.text(
        x_df - b * 0.05,
        base / 2,
        f"Df = {df:.2f} m",
        ha="right",
        va="center",
        fontsize=10,
        rotation=90,
        fontweight="bold",
        color="#153C70",
        zorder=10,
        bbox=dict(
            boxstyle="round,pad=0.35",
            facecolor="#F1F5F9",
            edgecolor="#94A3B8",
            linewidth=0.8,
            alpha=0.98,
        ),
    )

    # Cota de ancho en corte.
    y_ancho = base - h * 0.55

    ax2.annotate(
        "",
        xy=(0, y_ancho),
        xytext=(b, y_ancho),
        arrowprops=dict(
            arrowstyle="<->",
            color="#153C70",
        ),
    )

    ax2.text(
        b / 2,
        y_ancho - h * 0.12,
        f"B = {b:.2f} m",
        ha="center",
        va="top",
        fontsize=10,
        fontweight="bold",
        color="#153C70",
        zorder=10,
        bbox=dict(
            boxstyle="round,pad=0.35",
            facecolor="#F1F5F9",
            edgecolor="#94A3B8",
            linewidth=0.8,
            alpha=0.98,
        ),
    )

    ax2.text(
        b * 1.0, h * 0.15,
        "Terreno natural",
        fontsize=9,
        color="#426632",
    )

    ax2.set_xlim(-b * 0.53, b * 1.5)
    ax2.set_ylim(
        fondo - h * 0.4,
        tope_columna + h * 1.8,
    )
    ax2.axis("off")

    # -------------------------------------------------
    # DATOS Y RESULTADOS
    # -------------------------------------------------

    datos = (
        "PROPIEDADES DEL SUELO\n"
        f"Cohesión c: {c:.2f} kPa\n"
        f"Ángulo de fricción φ: {phi:.2f}°\n"
        f"Peso unitario γ: {gamma:.2f} kN/m³\n"
        f"Profundidad Df: {df:.2f} m"
    )

    resultados_txt = (
        "RESULTADOS DEL ANÁLISIS\n"
        f"q admisible: {qadm:.3f} kPa\n"
        f"q aplicada: {qaplicada:.3f} kPa\n"
        f"Q admisible: {qtotal:.3f} kN\n"
        f"FS disponible: {fs_disp:.3f}\n"
        f"Verificación: {'CUMPLE' if cumple else 'NO CUMPLE'}"
    )

    fig.text(
        0.09, 0.28,
        datos,
        fontsize=10,
        va="top",
        linespacing=1.5,
        bbox=dict(
            boxstyle="round,pad=0.65",
            facecolor="#EAF3FF",
            edgecolor="#A4BEDD",
        ),
    )

    fig.text(
        0.55, 0.28,
        resultados_txt,
        fontsize=10,
        va="top",
        linespacing=1.5,
        bbox=dict(
            boxstyle="round,pad=0.65",
            facecolor="#F0F7F0",
            edgecolor="#A4C7A4",
        ),
    )

    fig.text(
        0.5, 0.035,
        "ESQUEMA REFERENCIAL SIN ESCALA CONSTRUCTIVA. "
        "El espesor de la zapata y la columna son ilustrativos. "
        "No se verifica diseño estructural.",
        fontsize=8,
        ha="center",
        color="#64748B",
    )

    return fig
