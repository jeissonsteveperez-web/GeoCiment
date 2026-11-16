
# GeoCiment
### Aplicación de escritorio para el análisis de capacidad portante de cimentaciones superficiales

**Universidad Distrital Francisco José de Caldas**  
Facultad Tecnológica – Ingeniería Civil  
Programación II – Proyecto 02 – 2026

**Desarrollador:** Jeison Steven Pérez Maldonado  
**Modalidad:** Desarrollo individual con apoyo de inteligencia artificial.

---

## 1. Descripción

GeoCiment es una aplicación de escritorio desarrollada en Python para apoyar el análisis de capacidad portante de cimentaciones superficiales mediante la formulación clásica de Terzaghi.

El programa permite introducir parámetros geotécnicos, evaluar la capacidad portante, dimensionar zapatas cuadradas, visualizar resultados, almacenar proyectos y generar memorias de cálculo en Word.

Su finalidad es académica y educativa.

## 2. Funcionalidades

- Cálculo de capacidad portante última.
- Cálculo de capacidad portante admisible.
- Verificación de presión aplicada.
- Determinación del factor de seguridad disponible.
- Dimensionamiento numérico de zapatas cuadradas.
- Gráficas técnicas mediante Matplotlib.
- Almacenamiento de proyectos en SQLite.
- Búsqueda, recuperación y eliminación de proyectos.
- Generación automática de memorias Word.
- Ecuaciones matemáticas editables en Word.
- Validación de entradas y pruebas automatizadas.

## 3. Herramientas utilizadas

| Herramienta | Aplicación |
|---|---|
| Python | Lenguaje de programación |
| Flet | Interfaz gráfica |
| NumPy | Cálculo matemático y vectorizado |
| SciPy | Dimensionamiento numérico con brentq |
| Matplotlib | Generación de gráficas |
| SQLite | Almacenamiento de proyectos |
| docxtpl | Generación de memorias Word |
| math2docx | Ecuaciones matemáticas editables |
| pytest | Pruebas automatizadas |

## 4. Requisitos previos

Para ejecutar GeoCiment se necesita:

- Un computador compatible con las dependencias del proyecto.
- Python instalado.
- Visual Studio Code o una terminal de comandos.
- Conexión a internet para instalar las bibliotecas por primera vez.

Se recomienda utilizar Windows, que es el sistema en el cual se desarrolló el proyecto.

Se debe utilizar una versión de Python compatible con las versiones de las bibliotecas indicadas en `requirements.txt`.

## 5. Instalación paso a paso

### Paso 1. Obtener el proyecto

Descargar el repositorio desde GitHub mediante:

**Code → Download ZIP**

Descomprimir el archivo en una carpeta del computador.

### Paso 2. Abrir la carpeta

Abrir Visual Studio Code.

Seleccionar:

**Archivo → Abrir carpeta**

Buscar y seleccionar la carpeta `GeoCiment`.

### Paso 3. Abrir la terminal

En Visual Studio Code seleccionar:

**Terminal → Nuevo terminal**

### Paso 4. Crear el entorno virtual

Ejecutar:

```powershell
py -m venv .venv
```

### Paso 5. Activar el entorno

En PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, ejecutar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Después repetir el comando de activación.

### Paso 6. Instalar las bibliotecas

Ejecutar:

```powershell
python -m pip install -r requirements.txt
```

Esperar a que termine la instalación.

### Paso 7. Iniciar GeoCiment

Ejecutar:

```powershell
python main.py
```

Se abrirá la aplicación de escritorio.

**Nota:** No es necesario instalar nuevamente las bibliotecas cada vez que se utiliza el programa.

## 6. Uso de GeoCiment

### Realizar un cálculo

1. Abrir GeoCiment.
2. Escribir el nombre y la ubicación del proyecto.
3. Introducir las propiedades del suelo.
4. Introducir las dimensiones de la zapata.
5. Introducir la carga y el factor de seguridad.
6. Presionar "Calcular capacidad portante".
7. Revisar los resultados y la gráfica.

### Guardar un proyecto

Después de calcular, presionar "Guardar proyecto".

GeoCiment almacenará los datos mediante SQLite.

### Recuperar un proyecto

1. Seleccionar la pestaña "Historial".
2. Buscar el proyecto.
3. Presionar "Abrir".
4. Revisar los datos y los resultados recuperados.

### Generar una memoria Word

1. Realizar o recuperar un cálculo.
2. Presionar "Generar memoria Word".
3. Abrir la carpeta `salidas/reportes`.
4. Consultar el archivo generado.

El documento contiene datos, ecuaciones, resultados, gráfica y conclusiones.

## 7. Fundamento geotécnico

El modelo utiliza la formulación clásica de Terzaghi para capacidad portante de cimentaciones superficiales.

Se consideran los factores Nc, Nq y Nγ, que dependen del ángulo de fricción interna.

Se calcula la capacidad portante última, la capacidad admisible y la presión transmitida al suelo.

Para el dimensionamiento de zapatas cuadradas se utiliza el método numérico de Brent, implementado en SciPy.

La solución busca un ancho de cimentación que satisfaga la condición:

q_adm(B) = P / B²

El cálculo se realiza bajo hipótesis simplificadas de suelo homogéneo, carga vertical centrada, terreno horizontal y nivel freático suficientemente profundo.

## 8. Limitaciones

GeoCiment es una herramienta académica.

No sustituye un estudio geotécnico ni una memoria de diseño de cimentaciones.

El modelo no contempla:

- Asentamientos totales y diferenciales.
- Nivel freático cercano a la cimentación.
- Cargas excéntricas o inclinadas.
- Estratificación del suelo.
- Verificaciones estructurales de la zapata.
- Otras condiciones de falla no consideradas.

Los resultados deben interpretarse dentro de las hipótesis matemáticas establecidas.

## 9. Pruebas automatizadas

Desde la carpeta principal ejecutar:

```powershell
python -m pytest tests/test_modelo.py -v
```

El proyecto incluye cinco pruebas del modelo:

1. Factores de capacidad portante para phi = 0°.
2. Comparación con un ejercicio manual.
3. Capacidad portante de un suelo friccionante.
4. Dimensionamiento automático con SciPy.
5. Validación de dimensiones incorrectas.

## 10. Estructura del proyecto

```text
GeoCiment/
├── main.py
├── crear_plantilla.py
├── requirements.txt
├── README.md
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── modelo.py
│   ├── db.py
│   ├── graficas.py
│   └── reporte.py
├── plantillas/
│   └── memoria.docx
├── tests/
│   └── test_modelo.py
└── ejemplos/
    ├── memoria_ejemplo.docx
    └── capturas/
```

La base de datos y los reportes de trabajo se generan localmente.

## 11. Capturas de pantalla

### Interfaz principal

![Interfaz de cálculo](ejemplos/capturas/interfaz.png)

### Resultados y gráfica

![Resultados geotécnicos](ejemplos/capturas/resultados.png)

### Historial de proyectos

![Historial SQLite](ejemplos/capturas/historial.png)

## 12. Referencia bibliográfica

Terzaghi, K. (1943). *Theoretical Soil Mechanics*. John Wiley & Sons.

## 13. Desarrollo con apoyo de inteligencia artificial

GeoCiment fue desarrollado como proyecto académico de Programación II, utilizando inteligencia artificial como herramienta de apoyo para la estructuración del código, implementación de funcionalidades, depuración, documentación y pruebas.

La ejecución, integración, revisión y sustentación del proyecto corresponden al estudiante desarrollador.

## Validación del modelo geotécnico

El modelo de GeoCiment fue contrastado con el ejemplo
16.1 del texto de referencia utilizado en el proyecto,
correspondiente a una cimentación cuadrada de 2 × 2 m.

### Datos del ejercicio

- Cohesión: 20 kPa
- Ángulo de fricción: 25°
- Peso unitario: 16,5 kN/m³
- Profundidad de desplante: 1,5 m
- Factor de seguridad: 3

### Comparación de resultados

| Parámetro | Libro | GeoCiment |
|---|---:|---:|
| Nc | 25,13 | 25,13 |
| Nq | 12,72 | 12,72 |
| Nγ | 8,34 | 8,34 |
| Capacidad última (kPa) | 1078,29 | 1078,288 |
| Capacidad admisible (kPa) | 359,5 aprox. | 359,429 |
| Carga admisible (kN) | 1438 aprox. | 1437,717 |

Las pequeñas diferencias corresponden al redondeo
de los resultados presentados en el libro.

Los factores de capacidad portante fueron tomados
de la tabla 16.1 del mismo texto. Para valores
intermedios del ángulo de fricción se utiliza
interpolación lineal mediante NumPy.

La comparación se incorporó a las pruebas
automatizadas mediante pytest, obteniendo
seis pruebas aprobadas.

Esta validación corresponde a las hipótesis del
modelo implementado y no reemplaza las demás
verificaciones de diseño geotécnico.


## 14. Autor

**Jeison Steven Pérez Maldonado**

Ingeniería Civil  
Universidad Distrital Francisco José de Caldas  
Programación II – 2026
