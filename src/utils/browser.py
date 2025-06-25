from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions 
from selenium.webdriver.firefox.options import Options as FirefoxOptions 
from selenium.webdriver.edge.options import Options as EdgeOptions 

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager 
import logging
from datetime import datetime
import os

# Configurar logger
logger = logging.getLogger(__name__)

def get_driver(browser: str = "chrome", headless: bool = False, timeout: int = 30) -> webdriver:
    """
    Inicializa y retorna una instancia del WebDriver configurado
    
    Args:
        browser: Navegador a usar ('chrome', 'firefox', 'edge')
        headless: Si se ejecuta en modo sin cabeza (sin interfaz gráfica)
        timeout: Tiempo de espera implícito en segundos
    
    Returns:
        Instancia configurada del WebDriver
    """
    try:
        logger.info(f"Inicializando navegador {browser} (headless={headless})")
        
        if browser.lower() == "firefox":
            return _init_firefox(headless, timeout)
        elif browser.lower() == "edge":
            return _init_edge(headless, timeout)
        else:  # Default to Chrome
            return _init_chrome(headless, timeout)
            
    except Exception as e:
        logger.error(f"Error al inicializar el navegador {browser}: {str(e)}")
        raise

def _init_chrome(headless: bool, timeout: int) -> webdriver.Chrome:
    """Configura e inicializa ChromeDriver"""
    chrome_options = ChromeOptions() # Usamos ChromeOptions importado
    
    # Configuración básica
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--lang=es-ES")
    
    # Modo headless
    if headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
    
    # Opciones para evitar detección como bot
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
    # --- ARGUMENTOS ACTUALIZADOS Y MÁS AGRESIVOS PARA EVITAR NOTIFICACIONES Y POP-UPS ---
    chrome_options.add_experimental_option("prefs", {
        "credentials_enable_service": False,      # Evita la oferta de guardar contraseñas
        "profile.password_manager_enabled": False, # Deshabilita el gestor de contraseñas de Chrome
        "profile.default_content_setting_values.notifications": 2, # Deshabilita notificaciones de sitios web (pop-ups)
        "safeBrowse.enabled": False,           # Deshabilita Navegación Segura de Google (corrige 'safeBrowse' a 'safeBrowse')
        "safeBrowse.disable_download_protection": True, # Deshabilita la protección de descarga
        "security.enable_java": False,           # Deshabilita Java si aún lo tienes habilitado
        "download.prompt_for_download": False,   # No preguntar dónde guardar descargas
        "download.directory_upgrade": True,
        "plugins.plugins_disabled": ["Chrome PDF Viewer"], # Deshabilita plugins si causan problemas
        "plugins.always_open_pdf_externally": True, # Abrir PDFs externamente
        "autofill.enabled": False                # Deshabilita autocompletado de formularios
    })
    
    # Otros argumentos adicionales para suprimir UI y pop-ups
    chrome_options.add_argument("--no-sandbox") # Necesario en algunos entornos (ej. Linux/Docker)
    chrome_options.add_argument("--disable-dev-shm-usage") # Para entornos con poca RAM (ej. Docker)
    chrome_options.add_argument("--disable-browser-side-navigation") # Ayuda con "Element is not clickable"
    chrome_options.add_argument("--disable-features=EnableReaderMode") # Deshabilita el modo lector
    
    # Añadidos o re-confirmados para máxima supresión:
    chrome_options.add_argument("--disable-popup-blocking") # Deshabilita el bloqueador de pop-ups
    chrome_options.add_argument("--disable-component-update") # Previene actualizaciones en segundo plano
    chrome_options.add_argument("--disable-default-apps") # Deshabilita apps predeterminadas de Chrome
    chrome_options.add_argument("--disable-translate") # Deshabilita el traductor
    chrome_options.add_argument("--incognito") # Inicia Chrome en modo incógnito (a veces ayuda a aislar sesiones)
    chrome_options.add_argument("--no-first-run") # Para manejar los "primera vez ejecutando Chrome"
    chrome_options.add_argument("--disable-features=RendererCodeIntegrity") # Puede ayudar con ciertas protecciones

    # Obtener la última versión del driver automáticamente
    service = Service(ChromeDriverManager().install())
    
    # Inicializar el driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(timeout)
    
    # Ejecutar script para evitar detección (mantener al final)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    
    logger.info("ChromeDriver inicializado correctamente")
    return driver

def _init_firefox(headless: bool, timeout: int) -> webdriver.Firefox:
    """Configura e inicializa GeckoDriver (Firefox)"""
    firefox_options = FirefoxOptions() # Usamos FirefoxOptions importado
    
    # Configuración básica
    firefox_options.set_preference("intl.accept_languages", "es-ES")
    firefox_options.set_preference("dom.webnotifications.enabled", False) # Deshabilita notificaciones en Firefox
    
    # --- NUEVAS PREFERENCIAS PARA EVITAR NOTIFICACIONES DE SEGURIDAD Y BRECHAS DE DATOS EN FIREFOX ---
    firefox_options.set_preference("security.enable_java", False) # Deshabilita Java si está habilitado
    firefox_options.set_preference("browser.safeBrowse.enabled", False) # Deshabilita Navegación Segura (Firefox)
    firefox_options.set_preference("browser.safeBrowse.malware.enabled", False) # Deshabilita protección contra malware
    firefox_options.set_preference("signon.rememberSignons", False) # Deshabilita guardar contraseñas
    firefox_options.set_preference("security.insecure_field_warning.enabled", False) # Deshabilita advertencias de campos inseguros
    firefox_options.set_preference("extensions.enabledAddons", "") # Deshabilita extensiones
    firefox_options.set_preference("browser.translations.enabled", False) # Deshabilita el traductor

    # Modo headless
    if headless:
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")
    
    # Obtener la última versión del driver automáticamente
    service = Service(GeckoDriverManager().install())
    
    # Inicializar el driver
    driver = webdriver.Firefox(service=service, options=firefox_options)
    driver.maximize_window()
    driver.implicitly_wait(timeout)
    
    logger.info("GeckoDriver (Firefox) inicializado correctamente")
    return driver

def _init_edge(headless: bool, timeout: int) -> webdriver.Edge:
    """Configura e inicializa EdgeDriver"""
    edge_options = EdgeOptions() # Usamos EdgeOptions importado
    
    # Configuración básica
    edge_options.add_argument("--start-maximized")
    edge_options.add_argument("--lang=es-ES")
    
    # Modo headless
    if headless:
        edge_options.add_argument("--headless=new")
        edge_options.add_argument("--window-size=1920,1080")
    
    # Opciones para evitar detección como bot
    edge_options.add_argument('--disable-blink-features=AutomationControlled')
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option('useAutomationExtension', False)
    
    # --- NUEVOS ARGUMENTOS PARA EVITAR NOTIFICACIONES DE SEGURIDAD Y BRECHAS DE DATOS EN EDGE ---
    edge_options.add_experimental_option("prefs", {
        "credentials_enable_service": False,      # Evita la oferta de guardar contraseñas
        "profile.password_manager_enabled": False, # Deshabilita el gestor de contraseñas
        "profile.default_content_setting_values.notifications": 2, # Deshabilita notificaciones de sitios web (push)
        "safeBrowse.enabled": False,           # Deshabilita Navegación Segura de Google (corrige 'safeBrowse' a 'safeBrowse')
        "safeBrowse.disable_download_protection": True, # Deshabilita la protección de descarga
        "security.enable_java": False,           # Deshabilita Java si aún lo tienes habilitado
        "download.prompt_for_download": False,   # No preguntar dónde guardar descargas
        "download.directory_upgrade": True,
        "plugins.plugins_disabled": ["Edge PDF Viewer"], # Deshabilita plugins si causan problemas
        "plugins.always_open_pdf_externally": True, # Abrir PDFs externamente
        "autofill.enabled": False                # Deshabilita autocompletado de formularios
    })

    # Otros argumentos adicionales para suprimir UI y pop-ups
    edge_options.add_argument("--no-sandbox") # Necesario en algunos entornos (ej. Linux/Docker)
    edge_options.add_argument("--disable-dev-shm-usage") # Para entornos con poca RAM (ej. Docker)
    edge_options.add_argument("--disable-browser-side-navigation") # Ayuda con "Element is not clickable"
    edge_options.add_argument("--disable-features=EnableReaderMode") # Deshabilita el modo lector

    # Añadidos o re-confirmados para máxima supresión:
    edge_options.add_argument("--disable-popup-blocking") # Deshabilita el bloqueador de pop-ups
    edge_options.add_argument("--disable-component-update") # Previene actualizaciones en segundo plano
    edge_options.add_argument("--disable-default-apps") # Deshabilita apps predeterminadas de Edge
    edge_options.add_argument("--disable-translate") # Deshabilita el traductor
    edge_options.add_argument("--incognito") # Inicia Edge en modo incógnito (a veces ayuda a aislar sesiones)
    edge_options.add_argument("--no-first-run") # Para manejar los "primera vez ejecutando Edge"
    edge_options.add_argument("--disable-features=RendererCodeIntegrity") # Puede ayudar con ciertas protecciones
    
    # Obtener la última versión del driver automáticamente
    service = Service(EdgeChromiumDriverManager().install())
    
    # Inicializar el driver
    driver = webdriver.Edge(service=service, options=edge_options)
    driver.implicitly_wait(timeout)
    
    # Ejecutar script para evitar detección (mantener al final)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    
    logger.info("EdgeDriver inicializado correctamente")
    return driver

def take_screenshot(driver, test_name: str):
    """
    Toma un screenshot y lo guarda en el directorio de screenshots
    
    Args:
        driver: Instancia del WebDriver
        test_name: Nombre de la prueba para nombrar el archivo
    """
    try:
        # Crear directorio si no existe
        screenshot_dir = os.path.join(os.getcwd(), "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        
        # Generar nombre de archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{timestamp}.png"
        filepath = os.path.join(screenshot_dir, filename)
        
        # Tomar screenshot
        driver.save_screenshot(filepath)
        logger.info(f"Screenshot guardado: {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Error al tomar screenshot: {str(e)}")
        return None