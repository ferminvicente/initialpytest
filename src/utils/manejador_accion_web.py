from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from src.config.variables_globales import VariablesGlobales
import logging
import time

class manejadorAccionWeb:
    
    def __init__(self, driver: WebDriver, timeout: int = VariablesGlobales.TIMEOUT):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        self.logger = logging.getLogger(__name__)

    def _map_by_type(self, by_type: str) -> By:
        """Mapea string a objeto By de Selenium"""
        mapping = {
            "id": By.ID,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR,
            "name": By.NAME,
            "class": By.CLASS_NAME,
            "link": By.LINK_TEXT,
            "partial_link": By.PARTIAL_LINK_TEXT,
            "tag": By.TAG_NAME
        }
        by_type = by_type.lower()
        if by_type not in mapping:
            raise ValueError(f"Tipo de selector inválido: {by_type}")
        return mapping[by_type]

    def click(self, by_type: str, locator: str):
        by = self._map_by_type(by_type)
        element = self.wait.until(EC.element_to_be_clickable((by, locator)))
        self.logger.info(f"Click en elemento: {locator} ({by_type})")
        element.click()
        return self

    def go_url(self, url: str):
        self.logger.info(f"Navegando a URL: {url}")
        self.driver.get(url)
        return self     

    def send_keys(self, by_type: str, locator: str, text: str):
        by = self._map_by_type(by_type)
        element = self.wait.until(EC.visibility_of_element_located((by, locator)))
        self.logger.info(f"Escribiendo '{text}' en {locator} ({by_type})")
        element.clear()
        element.send_keys(text)
        return self

    def get_text(self, by_type: str, locator: str) -> str:
        by = self._map_by_type(by_type)
        element = self.wait.until(EC.visibility_of_element_located((by, locator)))
        return element.text

    def get_value(self, by_type: str, locator: str) -> str:
        by = self._map_by_type(by_type)
        element = self.wait.until(EC.visibility_of_element_located((by, locator)))
        return element.get_attribute("value")

    def copy_text(self, by_type: str, source_locator: str):
        text = self.get_text(by_type, source_locator)
        # Simulación de copiar al portapapeles (puede no funcionar siempre)
        self.driver.execute_script(f"navigator.clipboard.writeText('{text}')")
        self.logger.info(f"Texto copiado: {text}")
        return text

    def paste_text(self, by_type: str, target_locator: str):
        # NOTA: La siguiente línea puede fallar por permisos de portapapeles en JS
        self.driver.execute_script(
            f"document.querySelector('{target_locator}').value = navigator.clipboard.readText()"
        )
        self.logger.info("Texto pegado")
        return self

    def is_element_visible(self, by_type: str, locator: str) -> bool:
        try:
            by = self._map_by_type(by_type)
            return self.wait.until(EC.visibility_of_element_located((by, locator))) is not None
        except TimeoutException:
            return False

    def is_text_visible(self, text: str) -> bool:
        try:
            return self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "//*"), text))
        except TimeoutException:
            return False

    def wait_for_element(self, by_type: str, locator: str):
        by = self._map_by_type(by_type)
        self.wait.until(EC.visibility_of_element_located((by, locator)))
        return self

    def wait_for_text(self, text: str):
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "//body"), text))
        return self

    def wait_for_url_contains(self, url_part: str):
        self.wait.until(EC.url_contains(url_part))
        return self

    def take_screenshot(self, filename: str):
        self.driver.save_screenshot(filename)
        self.logger.info(f"Captura guardada: {filename}")
        return self

    def sleep(self, seconds: float):
        time.sleep(seconds)
        return self

    # Métodos de verificación con assert
    def verify_element_visible(self, by_type: str, locator: str, message: str = ""):
        visible = self.is_element_visible(by_type, locator)
        error_msg = message or f"Elemento {locator} no es visible"
        assert visible, error_msg
        self.logger.info(f"Elemento visible: {locator}")
        return self

    def verify_text_visible(self, text: str, message: str = ""):
        visible = self.is_text_visible(text)
        error_msg = message or f"Texto '{text}' no encontrado"
        assert visible, error_msg
        self.logger.info(f"Texto visible: '{text}'")
        return self

    def verify_page_title(self, expected_title: str):
        actual_title = self.driver.title
        assert actual_title == expected_title, f"Título esperado: '{expected_title}', actual: '{actual_title}'"
        self.logger.info(f"Título verificado: '{expected_title}'")
        return self

    def verify_url_contains(self, expected_url_part: str):
        actual_url = self.driver.current_url
        assert expected_url_part in actual_url, f"URL no contiene '{expected_url_part}', URL actual: '{actual_url}'"
        self.logger.info(f"URL contiene: '{expected_url_part}'")
        return self

    def verify_text_in_element(self, by_type: str, locator: str, expected_text: str):
        actual_text = self.get_text(by_type, locator)
        assert actual_text == expected_text, f"Texto esperado: '{expected_text}', actual: '{actual_text}'"
        self.logger.info(f"Texto verificado en {locator}: '{expected_text}'")
        return self

    def verify_value_in_element(self, by_type: str, locator: str, expected_value: str):
        actual_value = self.get_value(by_type, locator)
        assert actual_value == expected_value, f"Valor esperado: '{expected_value}', actual: '{actual_value}'"
        self.logger.info(f"Valor verificado en {locator}: '{expected_value}'")
        return self

    def verify_element_not_present(self, by_type: str, locator: str):
        try:
            by = self._map_by_type(by_type)
            self.wait.until(EC.presence_of_element_located((by, locator)))
            raise AssertionError(f"Elemento {locator} debería no estar presente")
        except TimeoutException:
            self.logger.info(f"Elemento {locator} no encontrado como se esperaba")
        return self

    def verify_element_not_visible(self, by_type: str, locator: str):
        visible = self.is_element_visible(by_type, locator)
        assert not visible, f"Elemento {locator} debería no ser visible"
        self.logger.info(f"Elemento {locator} no visible como se esperaba")
        return self
    def wait_for_element_to_be_clickable(self, by_type: str, locator: str):
        by = self._map_by_type(by_type)
        self.wait.until(EC.element_to_be_clickable((by, locator)))
        self.logger.info(f"Elemento {locator} es clickable")
        return self
