import pytest
from src.config.variables_globales import VariablesGlobales
from src.Locators.locators import Locators
import logging
import os
import sys

# Configuración del logger
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT_DIR)

logger = logging.getLogger(__name__)

def test_add_item_to_cart_and_verify(logged_in_accion_web): # ¡Importante: cambiamos 'accion_web' a 'logged_in_accion_web'!
    """
    Prueba que un usuario puede iniciar sesión, agregar un ítem al carrito y verificar su adición.
    El login es gestionado por el fixture 'logged_in_accion_web'.
    """
    logger.info("Iniciando prueba de agregar ítem al carrito (después del login automático).")

    # El navegador ya está abierto y el usuario ya está logueado por el fixture.
    # Paso 1: Verificar que estamos en la página de inventario
    # (Esto confirma que el login a través del fixture fue exitoso)
    logged_in_accion_web.wait_for_element(Locators.INVENTORY_CONTAINER)
    logger.info("Esperando que el contenedor de inventario sea visible después del login.")
    assert logged_in_accion_web.is_element_visible(Locators.INVENTORY_CONTAINER), \
    logger.info("Inventario visible, confirmando login exitoso.")

    # --- Pasos para Agregar al carrito y verificar ---

    # Paso 2: Hacer clic en el botón "Add to cart" para un producto específico
    logged_in_accion_web.wait_for_element_to_be_clickable(Locators.ADD_TO_CART_SAUCE_LABS_BACKPACK)
    logged_in_accion_web.click(Locators.ADD_TO_CART_SAUCE_LABS_BACKPACK)
    logger.info("Producto 'Sauce Labs Backpack' agregado al carrito.")

    # Paso 3: Verificar que el contador del carrito muestra '1'
    cart_items_count = logged_in_accion_web.get_text(Locators.SHOPPING_CART_BADGE)
    assert cart_items_count == "1", \
        f"ERROR: Se esperaba 1 ítem en el carrito, pero se encontró: {cart_items_count}"
    logger.info(f"El contador del carrito muestra: {cart_items_count} ítem(s).")

    # Paso 4: Navegar a la página del carrito
    logged_in_accion_web.click(Locators.SHOPPING_CART_LINK)
    logger.info("Navegado a la página del carrito.")

    # Paso 5: Verificar que el ítem agregado aparece en la lista del carrito
    assert logged_in_accion_web.is_element_visible(Locators.CART_ITEM_SAUCE_LABS_BACKPACK), \
        "ERROR: El 'Sauce Labs Backpack' no es visible en la página del carrito."
    logger.info("Producto 'Sauce Labs Backpack' verificado en el carrito.")

    logger.info("Prueba de agregar ítem al carrito completada exitosamente.")