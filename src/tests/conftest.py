import pytest
import logging
import allure 
from allure_commons.types import AttachmentType 
from src.utils.browser import get_driver
from src.config.variables_globales import VariablesGlobales
from src.Locators.locators import Locators
from src.utils.AccionWeb import AccionWeb

# Configurar logger (opcional, pero buena práctica si no lo tienes ya en una configuración global)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def accion_web(request): # ¡IMPORTANTE! Añade 'request' como argumento aquí
    """
    Fixture que inicializa el WebDriver y la instancia de AccionWeb.
    """
    driver = get_driver()
    accion_web_instance = AccionWeb(driver)
    
    # --- ¡LA CLAVE! Almacenar el driver en el objeto 'item' de Pytest ---
    # Esto permite que el hook 'pytest_runtest_makereport' acceda al driver activo.
    # 'request.node' representa el ítem de la prueba actual que está usando esta fixture.
    request.node._driver = driver 
    
    yield accion_web_instance # El test se ejecuta aquí

    # --- Limpieza (teardown) del fixture: Se ejecuta después de que el test termina ---
    if hasattr(request.node, '_driver'):
        # Si el driver fue almacenado, lo eliminamos por limpieza
        del request.node._driver
    
    driver.quit()
    logger.info("Navegador cerrado después de la prueba.")


@pytest.fixture(scope="function")
def logged_in_accion_web(accion_web): # Este fixture *depende* de 'accion_web'
    """
    Fixture que realiza el login en la aplicación y luego proporciona la instancia de AccionWeb
    con la sesión ya iniciada.
    """
    logger.info("Iniciando proceso de login a través del fixture 'logged_in_accion_web'.")

    # 1. Navegar a la página de login (la instancia de accion_web ya está disponible)
    accion_web.go_url(VariablesGlobales.BASE_URL)

    # 2. Realizar login usando los localizadores y credenciales
    (accion_web
     .send_keys(Locators.USERNAME_INPUT, VariablesGlobales.USERNAME)
     .send_keys(Locators.PASSWORD_INPUT, VariablesGlobales.PASSWORD)
     .click(Locators.LOGIN_BUTTON))

    # 3. Verificar que el login fue exitoso
    accion_web.wait_for_element(Locators.APP_LOGO) # Espera a que el logo de la app sea visible
    assert accion_web.is_element_visible(Locators.APP_LOGO), "No se mostró el inventario después del login"
    
    # 4. Registrar el éxito del login
    logger.info("Login completado exitosamente por el fixture.")

    yield accion_web # Entrega la instancia de AccionWeb (ya logueada) para las pruebas

# --- HOOK DE PYTEST PARA CAPTURAS DE PANTALLA EN CADA TEST ---
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook de Pytest para adjuntar capturas de pantalla a los reportes Allure
    para cada prueba, independientemente de si pasa o falla.
    """
    # Ejecuta el resto del hook para obtener el 'report' del test
    outcome = yield
    report = outcome.get_result()

    # Solo si estamos en la fase de "llamada" (ejecución real del test)
    # y el test ha terminado (ya sea pasado o fallado)
    if report.when == "call": 
        # --- VERIFICACIÓN CRÍTICA: Asegurarse de que el driver esté disponible ---
        # El driver se almacena en `item._driver` por la fixture `accion_web`
        if hasattr(item, '_driver') and item._driver:
            driver = item._driver
            try:
                # Toma la captura de pantalla como bytes PNG
                screenshot_bytes = driver.get_screenshot_as_png()
                
                # Adjuntar la captura a Allure
                allure.attach(
                    screenshot_bytes,
                    name=f"Captura - {'EXITOSA' if report.passed else 'FALLIDA'}: {item.name}",
                    attachment_type=AttachmentType.PNG
                )
                logger.info(f"Captura de pantalla adjuntada para el test: {item.name} ({'EXITOSA' if report.passed else 'FALLIDA'})")
            except Exception as e:
                # Si hay un error al tomar o adjuntar, se registrará aquí
                logger.error(f"Error al tomar o adjuntar captura de pantalla para {item.name}: {e}")
        else:
            # Si el driver no se encuentra, se registrará una advertencia
            logger.warning(f"No se encontró el driver en el hook para {item.name}. No se pudo tomar captura de pantalla.")