from dataclasses import dataclass
import logging

@dataclass
class VariablesGlobales:
    BASE_URL: str = "https://www.saucedemo.com"
    BROWSER: str = "chrome"
    HEADLESS: bool = False
    TIMEOUT: int = 10
    DRIVER_PATH: str = "C:\initialpytest\drivers\chrome-win32\chromedriver.exe"
    
    # Credenciales de usuario
    # Estas credenciales son para el sitio de prueba de SauceDemo
    USERNAME: str = "standard_user"
    PASSWORD: str = "secret_sauce"

    # Logger configurado
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
