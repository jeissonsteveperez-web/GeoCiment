
"""
GeoCiment - Aplicación de escritorio
Universidad Distrital Francisco José de Caldas
Programación II - Proyecto 02
"""

import io
import math

import flet as ft
import matplotlib.pyplot as plt


from app.reporte import generar_memoria

from app.modelo import capacidad_portante, dimensionar_zapata
from app.graficas import grafica_capacidad

from app.db import (
    inicializar_db,
    guardar_proyecto,
    listar_proyectos,
    obtener_proyecto,
    eliminar_proyecto,
)

def main(page: ft.Page):
    inicializar_db()

    ultimo_calculo = {
        "entradas": None,
        "resultados": None,
        "proyecto_id": None,
    }
    page.title = "GeoCiment - Capacidad Portante"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT

    # ------------------------------------------------
    # CAMPOS DE ENTRADA
    nombre_proyecto = ft.TextField(
        label="Nombre del proyecto",
        value="Proyecto de ejemplo",
        width=350,
    )

    ubicacion_proyecto = ft.TextField(
        label="Ubicación del proyecto",
        value="Bogotá, Colombia",
        width=350,
    )
    # ------------------------------------------------

    def campo(nombre, valor):
        return ft.TextField(
            label=nombre,
            value=str(valor),
            width=230,
        )

    cohesion = campo("Cohesión c (kPa)", 10)
    friccion = campo("Ángulo de fricción φ (°)", 30)
    gamma = campo("Peso unitario γ (kN/m³)", 18)
    ancho = campo("Ancho B (m)", 2)
    largo = campo("Largo L (m)", 2)
    profundidad = campo("Profundidad Df (m)", 1.5)
    carga = campo("Carga vertical P (kN)", 600)
    seguridad = campo("Factor de seguridad FS", 3)

    campos = [
        cohesion, friccion, gamma, ancho,
        largo, profundidad, carga, seguridad
    ]

    # ------------------------------------------------
    # RESULTADOS
    # ------------------------------------------------

    resultados = ft.Column(spacing=8)

    grafica = ft.Image(
        src=b"",
        width=850,
        height=450,
        fit=ft.BoxFit.CONTAIN,
        visible=False,
    )

    mensaje = ft.Text(
        "Introduce los datos y presiona Calcular.",
        color=ft.Colors.BLUE_700,
    )

    # ------------------------------------------------
    # FUNCIÓN DE CÁLCULO
    # ------------------------------------------------

    def calcular(e):
        try:
            valores = []

            for control in campos:
                texto = (control.value or "").strip()
                if not texto:
                    raise ValueError(
                        f"El campo '{control.label}' está vacío."
                    )

                numero = float(texto.replace(",", "."))

                if not math.isfinite(numero):
                    raise ValueError(
                        f"El campo '{control.label}' debe ser finito."
                    )

                valores.append(numero)

            c, phi, g, b, l, df, p, fs = valores

            if c < 0 or df < 0:
                raise ValueError(
                    "La cohesión y la profundidad no pueden ser negativas."
                )

            if not 0 <= phi < 45:
                raise ValueError(
                    "El ángulo de fricción debe estar entre 0 y 45°."
                )

            if min(g, b, l, p, fs) <= 0:
                raise ValueError(
                    "Gamma, dimensiones, carga y FS deben ser positivos."
                )

            if b > l:
                raise ValueError(
                    "El ancho B no puede superar el largo L."
                )

            # Modelo geotécnico
 # Un cálculo nuevo debe guardarse como registro nuevo.
            ultimo_calculo["proyecto_id"] = None

            r = capacidad_portante(
                c, phi, g, b, l, df, p, fs
            )

            # Dimensionamiento cuadrado con SciPy
            b_min = dimensionar_zapata(
                c, phi, g, df, p, fs
            )
            ultimo_calculo["entradas"] = {
                "c": c,
                "phi": phi,
                "gamma": g,
                "b": b,
                "l": l,
                "df": df,
                "carga": p,
                "fs": fs,
            }

            ultimo_calculo["resultados"] = {
                **r,
                "ancho_minimo": b_min,
                "area_minima": b_min ** 2,
            }

            # Mostrar resultados
            resultados.controls = [
                ft.Text(
                    "RESULTADOS DEL ANÁLISIS",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(f"Nc: {r['Nc']:.3f}"),
                ft.Text(f"Nq: {r['Nq']:.3f}"),
                ft.Text(f"Nγ: {r['Ngamma']:.3f}"),
                ft.Divider(),
                ft.Text(
                    f"Capacidad última: {r['qult']:.3f} kPa"
                ),
                ft.Text(
                    f"Capacidad admisible: {r['qadm']:.3f} kPa"
                ),
                ft.Text(
                    f"Presión aplicada: {r['qaplicada']:.3f} kPa"
                ),
                ft.Text(
                    f"FS disponible: {r['fs_disponible']:.3f}"
                ),
                ft.Divider(),
                ft.Text(
                    "CUMPLE POR CAPACIDAD PORTANTE"
                    if r["cumple"]
                    else "NO CUMPLE POR CAPACIDAD PORTANTE",
                    size=17,
                    weight=ft.FontWeight.BOLD,
                    color=(
                        ft.Colors.GREEN_700
                        if r["cumple"]
                        else ft.Colors.RED_700
                    ),
                ),
                ft.Text(
                    f"Ancho mínimo de zapata cuadrada: {b_min:.3f} m"
                ),
                ft.Text(
                    f"Área mínima cuadrada: {b_min**2:.3f} m²"
                ),
            ]

            # Crear gráfica usando Matplotlib
            figura = grafica_capacidad(
                c, phi, g, b, l, df, p, fs
            )

            buffer = io.BytesIO()

            try:
                figura.savefig(
                    buffer,
                    format="png",
                    dpi=140,
                    bbox_inches="tight",
                )
            finally:
                plt.close(figura)

            grafica.src = buffer.getvalue()
            grafica.visible = True

            mensaje.value = "Cálculo realizado correctamente."
            mensaje.color = ft.Colors.GREEN_700

        except (ValueError, OverflowError, ZeroDivisionError) as error:
            ultimo_calculo["entradas"] = None
            ultimo_calculo["resultados"] = None
            ultimo_calculo["proyecto_id"] = None  
            resultados.controls.clear()
            grafica.visible = False
            grafica.src = None

            mensaje.value = f"Error: {error}"
            mensaje.color = ft.Colors.RED_700

        except Exception as error:
            resultados.controls.clear()
            grafica.visible = False
            grafica.src = None

            mensaje.value = (
                f"No se pudo completar el cálculo: {error}"
            )
            mensaje.color = ft.Colors.RED_700

        page.update()

    def guardar_calculo(e):
        """Guarda el último cálculo en SQLite."""

        try:
            if ultimo_calculo["resultados"] is None:
                raise ValueError(
                    "Primero debes realizar un cálculo."
                )

            nombre = (nombre_proyecto.value or "").strip()
            ubicacion = (ubicacion_proyecto.value or "").strip()

            if not nombre:
                raise ValueError(
                    "Escribe un nombre para el proyecto."
                )

            proyecto_id = ultimo_calculo["proyecto_id"]

            if proyecto_id is None:
                proyecto_id = guardar_proyecto(
                    nombre,
                    ubicacion,
                    ultimo_calculo["entradas"],
                    ultimo_calculo["resultados"],
                )

                ultimo_calculo["proyecto_id"] = proyecto_id

            mensaje.value = (
                f"Proyecto guardado correctamente. "
                f"Identificador: {proyecto_id}"
            )
            mensaje.color = ft.Colors.GREEN_700

        except (ValueError, TypeError) as error:
            mensaje.value = f"Error: {error}"
            mensaje.color = ft.Colors.RED_700

        except Exception as error:
            mensaje.value = f"Error al guardar: {error}"
            mensaje.color = ft.Colors.RED_700

        page.update()


    def exportar_memoria(e):
        """
        Genera una memoria Word usando el proyecto
        guardado, sin duplicar registros en SQLite.
        """

        try:
            if ultimo_calculo["resultados"] is None:
                raise ValueError(
                    "Primero debes realizar un cálculo."
                )

            proyecto_id = ultimo_calculo["proyecto_id"]

            # Guardar una sola vez si todavía no existe.
            if proyecto_id is None:
                nombre = (nombre_proyecto.value or "").strip()
                ubicacion = (
                    ubicacion_proyecto.value or ""
                ).strip()

                if not nombre:
                    raise ValueError(
                        "Ingresa el nombre del proyecto."
                    )

                proyecto_id = guardar_proyecto(
                    nombre,
                    ubicacion,
                    ultimo_calculo["entradas"],
                    ultimo_calculo["resultados"],
                )

                ultimo_calculo["proyecto_id"] = proyecto_id

            # Generar Word utilizando el ID existente.
            ruta = generar_memoria(proyecto_id)

            mensaje.value = (
                f"Memoria generada correctamente.\n"
                f"Proyecto ID: {proyecto_id}\n"
                f"Archivo: {ruta}"
            )

            mensaje.color = ft.Colors.GREEN_700

        except Exception as error:
            mensaje.value = (
                f"Error al generar memoria: {error}"
            )
            mensaje.color = ft.Colors.RED_700

        page.update()
    

    # ------------------------------------------------
    # VISTA PRINCIPAL
    # ------------------------------------------------

    vista_calculo = ft.Column(
        controls=[
            ft.Text(
                "Identificación del proyecto",
                size=18,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Row(
                [nombre_proyecto, ubicacion_proyecto],
                wrap=True,
            ),
            ft.Divider(),
            ft.Text(
                "Análisis de capacidad portante",
                size=23,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Text(
                "Método de Terzaghi - Zapatas superficiales"
            ),
            ft.Text(
                "Modelo académico: suelo homogéneo, carga "
                "vertical centrada y nivel freático profundo.",
                color=ft.Colors.GREY_700,
            ),
            ft.Divider(),

            ft.Text(
                "1. Propiedades del suelo",
                size=18,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Row(
                [cohesion, friccion, gamma],
                wrap=True,
            ),

            ft.Text(
                "2. Geometría de la cimentación",
                size=18,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Row(
                [ancho, largo, profundidad],
                wrap=True,
            ),

            ft.Text(
                "3. Carga y seguridad",
                size=18,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Row(
                [carga, seguridad],
                wrap=True,
            ),

            ft.FilledButton(
                content="CALCULAR CAPACIDAD PORTANTE",
                icon=ft.Icons.CALCULATE,
                on_click=calcular,
            ),
            ft.FilledButton(
                content="GUARDAR PROYECTO",
                icon=ft.Icons.SAVE,
                on_click=guardar_calculo,
            ),
             ft.FilledButton(
                content="GENERAR MEMORIA WORD",
                icon=ft.Icons.DESCRIPTION,
                on_click=exportar_memoria,
            ),
            mensaje,
            ft.Divider(),
            resultados,
            grafica,
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=15,
    )

    # ------------------------------------------------
    # SEGUNDA VISTA
    # ------------------------------------------------

   
    # ------------------------------------------------
    # HISTORIAL DE PROYECTOS - SQLITE
    # ------------------------------------------------

    buscador = ft.TextField(
        label="Buscar proyecto por nombre",
        width=350,
    )

    lista_historial = ft.Column(spacing=10)

    aviso_historial = ft.Text(
        "Consulta los proyectos almacenados.",
        color=ft.Colors.BLUE_700,
    )

    def cargar_historial(e=None):
        """Consulta SQLite y actualiza la lista."""

        try:
            proyectos = listar_proyectos(
                (buscador.value or "").strip()
            )

            lista_historial.controls.clear()

            if not proyectos:
                lista_historial.controls.append(
                    ft.Text("No se encontraron proyectos.")
                )

            for proyecto in proyectos:
                pid = proyecto["id"]

                fila = ft.Column(
                    controls=[
                        ft.Text(
                            f"{proyecto['nombre']} - ID {pid}",
                            weight=ft.FontWeight.BOLD,
                            size=16,
                        ),
                        ft.Text(
                            f"Ubicación: "
                            f"{proyecto['ubicacion'] or 'No indicada'}"
                        ),
                        ft.Text(
                            f"Fecha: {proyecto['fecha']}"
                        ),
                        ft.Row(
                            controls=[
                                ft.Button(
                                    content="Abrir",
                                    icon=ft.Icons.FOLDER_OPEN,
                                    on_click=lambda e, id=pid:
                                        abrir_proyecto(id),
                                ),
                                ft.Button(
                                    content="Eliminar",
                                    icon=ft.Icons.DELETE,
                                    on_click=lambda e, id=pid:
                                        solicitar_eliminacion(id),
                                ),
                            ],
                            wrap=True,
                        ),
                        ft.Divider(),
                    ],
                    spacing=5,
                )

                lista_historial.controls.append(fila)

            aviso_historial.value = (
                f"Proyectos encontrados: {len(proyectos)}"
            )
            aviso_historial.color = ft.Colors.BLUE_700

        except Exception as error:
            aviso_historial.value = (
                f"Error al consultar proyectos: {error}"
            )
            aviso_historial.color = ft.Colors.RED_700

        page.update()

    def abrir_proyecto(proyecto_id):
        """Recupera los datos de un proyecto guardado."""

        try:
            proyecto = obtener_proyecto(proyecto_id)

            if not proyecto or not proyecto["calculos"]:
                raise ValueError(
                    "El proyecto no contiene cálculos."
                )

            datos = proyecto["calculos"][-1]["entradas"]

            nombre_proyecto.value = proyecto["nombre"]
            ubicacion_proyecto.value = (
                proyecto["ubicacion"] or ""
            )

            cohesion.value = str(datos["c"])
            friccion.value = str(datos["phi"])
            gamma.value = str(datos["gamma"])
            ancho.value = str(datos["b"])
            largo.value = str(datos["l"])
            profundidad.value = str(datos["df"])
            carga.value = str(datos["carga"])
            seguridad.value = str(datos["fs"])

            # Recalcular para actualizar resultados y gráfica.
            calcular(None)
            # Asociar el cálculo con el proyecto recuperado.
            if ultimo_calculo["resultados"] is not None:
                ultimo_calculo["proyecto_id"] = proyecto_id

            cambiar_vista(0)

            if ultimo_calculo["resultados"] is not None:
                mensaje.value = (
                    f"Proyecto '{proyecto['nombre']}' "
                    f"recuperado correctamente."
                )
                mensaje.color = ft.Colors.GREEN_700

        except Exception as error:
            import traceback
            traceback.print_exc()

            aviso_historial.value = (
                f"No se pudo abrir el proyecto: {error}"
            )
            aviso_historial.color = ft.Colors.RED_700
        page.update()

    # Confirmación de eliminación dentro del historial.
    confirmacion = ft.Column(spacing=8)

    def solicitar_eliminacion(proyecto_id):
        """Solicita confirmación antes de borrar."""

        confirmacion.controls = [
            ft.Text(
                f"¿Deseas eliminar el proyecto ID "
                f"{proyecto_id}?",
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.RED_700,
            ),
            ft.Text(
                "Esta acción eliminará también "
                "sus cálculos y no se puede deshacer."
            ),
            ft.Row(
                controls=[
                    ft.Button(
                        content="Sí, eliminar",
                        on_click=lambda e:
                            confirmar_eliminacion(proyecto_id),
                    ),
                    ft.Button(
                        content="Cancelar",
                        on_click=cancelar_eliminacion,
                    ),
                ],
            ),
        ]

        page.update()

    def cancelar_eliminacion(e=None):
        confirmacion.controls.clear()
        page.update()

    def confirmar_eliminacion(proyecto_id):
        """Elimina el proyecto después de confirmar."""

        try:
            eliminado = eliminar_proyecto(proyecto_id)
            confirmacion.controls.clear()

            cargar_historial()

            aviso_historial.value = (
                "Proyecto eliminado correctamente."
                if eliminado
                else "El proyecto ya no existe."
            )
            aviso_historial.color = ft.Colors.GREEN_700

        except Exception as error:
            aviso_historial.value = (
                f"Error al eliminar: {error}"
            )
            aviso_historial.color = ft.Colors.RED_700

        page.update()

    vista_historial = ft.Column(
        controls=[
            ft.Text(
                "Historial de proyectos",
                size=24,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Text(
                "Consulta y recupera los cálculos "
                "almacenados en SQLite."
            ),
            ft.Row(
                controls=[
                    buscador,
                    ft.Button(
                        content="Buscar",
                        icon=ft.Icons.SEARCH,
                        on_click=cargar_historial,
                    ),
                    ft.Button(
                        content="Actualizar",
                        icon=ft.Icons.REFRESH,
                        on_click=cargar_historial,
                    ),
                ],
                wrap=True,
            ),
            aviso_historial,
            confirmacion,
            lista_historial,
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )


    # ------------------------------------------------
    # NAVEGACIÓN
    # ------------------------------------------------

    contenido = ft.Container(expand=True)

    def cambiar_vista(indice):
        if indice == 0:
            contenido.content = vista_calculo
        else:
            contenido.content = vista_historial
            cargar_historial()

        page.update()

    barra = ft.Row(
        controls=[
            ft.Button(
                content="Cálculo",
                icon=ft.Icons.CALCULATE,
                on_click=lambda e: cambiar_vista(0),
            ),
            ft.Button(
                content="Historial",
                icon=ft.Icons.HISTORY,
                on_click=lambda e: cambiar_vista(1),
            ),
        ],
    )

    cambiar_vista(0)

    page.add(
        ft.Text(
            "GEOCIMENT",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_900,
        ),
        ft.Text(
            "Software académico de ingeniería geotécnica"
        ),
        barra,
        contenido,
    )


if __name__ == "__main__":
    ft.run(main)
