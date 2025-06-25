# initialpytest

# Automatización de Pruebas Web con Selenium  + Python - Funcionalidad "Agregar al Carrito"

Este proyecto contiene la automatización de pruebas para la funcionalidad de **"Agregar Producto al Carrito de Compras"** en una aplicación web, utilizando **Python** y el *framework* de automatización **Selenium WebDriver**.

El objetivo principal es asegurar que los usuarios puedan buscar productos, añadirlos al carrito, actualizar las cantidades y que el carrito refleje correctamente los elementos seleccionados y sus totales.

---

## Características Automatizadas

* **Navegación de Productos:** Búsqueda y visualización de detalles de productos.
* **Adición al Carrito:** Añadir uno o varios productos al carrito de compras.
* **Verificación del Carrito:** Validar que los productos y los totales se reflejan correctamente en el carrito.

---

## Estructura del Proyecto

La organización del proyecto sigue el patrón de diseño **Page Object Model (POM)** para mejorar la mantenibilidad, reutilización del código y legibilidad de los tests.

¡Mil disculpas! Tienes toda la razón, me equivoqué al mezclar los proyectos. Mi intención era darte un README.md general para tu repositorio AutomatizacionQA que contiene ambos proyectos (API y Web), pero me concentré demasiado en esa estructura.

Entiendo que ahora mismo necesitas el README.md específico para el proyecto de automatización web de "agregar producto al carrito", que es el que estás intentando subir.

Aquí tienes un README.md nuevo y enfocado exclusivamente en ese tipo de proyecto web de Selenium.

Markdown

# Automatización de Pruebas Web con Selenium - Funcionalidad "Agregar al Carrito"

Este proyecto contiene la automatización de pruebas para la funcionalidad de **"Agregar Producto al Carrito de Compras"** en una aplicación web, utilizando **Python** y el *framework* de automatización **Selenium WebDriver**.

El objetivo principal es asegurar que los usuarios puedan buscar productos, añadirlos al carrito, actualizar las cantidades y que el carrito refleje correctamente los elementos seleccionados y sus totales.

---

## Características Automatizadas

* **Navegación de Productos:** Búsqueda y visualización de detalles de productos.
* **Adición al Carrito:** Añadir uno o varios productos al carrito de compras.
* **Actualización de Cantidad:** Modificar la cantidad de productos en el carrito.
* **Eliminación de Productos:** Remover ítems del carrito.
* **Verificación del Carrito:** Validar que los productos y los totales se reflejan correctamente en el carrito.

---

## Estructura del Proyecto

La organización del proyecto sigue el patrón de diseño **Page Object Model (POM)** para mejorar la mantenibilidad, reutilización del código y legibilidad de los tests.
.
└── src/
    ├── config/          # Contiene archivos de configuración (ej: URLs, credenciales, entornos).
    ├── Locators/        # Almacena los localizadores de elementos UI (CSS, XPath, IDs).
    ├── tests/           # Contiene todos los casos de prueba automatizados (ej: usando Pytest).
    ├── utils/           # Módulos con funciones de utilidad y helpers reutilizables.
    ├── __init__.py      # Indica que 'src' es un paquete de Python.
    ├── main.py          # Punto de entrada principal para ejecutar la automatización.
    └── requirements.txt # Lista de las dependencias de Python para el proyecto.

    ## Configuración del Entorno y Ejecución de Pruebas

Sigue estos pasos para configurar tu entorno y ejecutar los tests de automatización web.

### 1. Clonar el Repositorio

Si este proyecto es parte de un repositorio Git   asegúrate de que estás en la carpeta `initialpytest` después de clonarlo:

```bash
# Ejemplo si el proyecto es una subcarpeta dentro de un repositorio principal
git clone <URL_DEL_REPOSITORIO_PRINCIPAL>
cd <NOMBRE_DEL_REPOSITORIO_PRINCIPAL>/SeleniumWebProject
```
---
2. Configurar y Activar el Entorno Virtual
Es fundamental usar un entorno virtual para aislar las dependencias del proyecto.
```bash
# Crea el entorno virtual (solo la primera vez)
python -m venv venv

# Activa el entorno virtual (para Windows PowerShell)
.\venv\Scripts\Activate.ps1
# O para Git Bash/macOS/Linux
source venv/bin/activate

```
---
3. Instalar Dependencias del Proyecto
Con el entorno virtual activado, instala todas las librerías necesarias especificadas en requirements.txt:
```bash
pip install -r requirements.txt
```
---
4. Descargar y Configurar el WebDriver del Navegador
Este proyecto utiliza ChromeDriver para automatizar Google Chrome.

Verifica tu versión de Chrome: Abre Chrome, ve a chrome://version/ y anota tu versión exacta.

Descarga el ChromeDriver compatible: Ve a la página oficial de descargas de ChromeDriver: https://chromedriver.chromium.org/downloads. Descarga la versión que coincida con la tuya.

Coloca el Driver: Guarda el archivo chromedriver.exe (o el equivalente para tu OS) dentro de la carpeta SeleniumWebProject/drivers/.
```bash
python -m pytest tests/ --alluredir=reports/allure-results -v
```
---


