from selenium.webdriver.common.by import By

class Locators:
    # Localizadores para el flujo de login
    USERNAME_INPUT = ('id', 'user-name')
    PASSWORD_INPUT = ('id', 'password')
    LOGIN_BUTTON = ('id', 'login-button')
    ERROR_MESSAGE = ('css', 'h3[data-test="error"]')
    APP_LOGO = ('class', 'app_logo')

    # Localizadores para el flujo del carrito
    INVENTORY_CONTAINER = ('id', 'inventory_container')
    ADD_TO_CART_SAUCE_LABS_BACKPACK = ('id', 'add-to-cart-sauce-labs-backpack')
    SHOPPING_CART_BADGE = ('class', 'shopping_cart_badge')
    SHOPPING_CART_LINK = ('class', 'shopping_cart_link')
    CART_ITEM_SAUCE_LABS_BACKPACK = ('id', 'item_4_title_link')
    # ... asegúrate de tener este también, que se usó en el test
    # Si 'is_visible' usa 'id' como el tipo de localizador para 'inventory_container', entonces es correcto.