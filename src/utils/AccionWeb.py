from src.utils.manejador_accion_web import manejadorAccionWeb


class AccionWeb:

    def __init__(self, driver):
        self.manejadorAccionWeb = manejadorAccionWeb(driver)


    # Métodos que realizan acciones (devuelven self para encadenar)
    def click(self, locator_tuple):
        self.manejadorAccionWeb.click(*locator_tuple)
        return self

    def go_url(self, url):
        self.manejadorAccionWeb.go_url(url)
        return self

    def send_keys(self, locator_tuple, text):
        self.manejadorAccionWeb.send_keys(*locator_tuple, text)
        return self

    def copy_text(self, source_locator_tuple):
        self.manejadorAccionWeb.copy_text(*source_locator_tuple)
        return self

    def paste_text(self, target_locator_tuple):
        self.manejadorAccionWeb.paste_text(*target_locator_tuple)
        return self

    # Métodos que retornan valores (no devuelven self)
    def get_text(self, locator_tuple):
        return self.manejadorAccionWeb.get_text(*locator_tuple)

    def get_value(self, locator_tuple):
        return self.manejadorAccionWeb.get_value(*locator_tuple)

    def is_element_visible(self, locator_tuple):
        return self.manejadorAccionWeb.is_element_visible(*locator_tuple)

    def is_text_visible(self, text):
        return self.manejadorAccionWeb.is_text_visible(text)

    # Métodos de espera, retornan valores o resultados (no devuelven self)
    def wait_for_element(self, locator_tuple):
        return self.manejadorAccionWeb.wait_for_element(*locator_tuple)

    def wait_for_text(self, text):
        return self.manejadorAccionWeb.wait_for_text(text)

    def wait_for_element_to_disappear(self, locator_tuple):
        return self.manejadorAccionWeb.wait_for_element_to_disappear(*locator_tuple)

    def wait_for_text_to_disappear(self, text):
        return self.manejadorAccionWeb.wait_for_text_to_disappear(text)

    def wait_for_page_load(self):
        return self.manejadorAccionWeb.wait_for_page_load()

    def wait_for_page_title(self, title):
        return self.manejadorAccionWeb.wait_for_page_title(title)

    def wait_for_page_url(self, url):
        return self.manejadorAccionWeb.wait_for_page_url(url)

    def wait_for_page_source(self, source):
        return self.manejadorAccionWeb.wait_for_page_source(source)

    def wait_for_element_to_be_clickable(self, locator_tuple):
        return self.manejadorAccionWeb.wait_for_element_to_be_clickable(*locator_tuple)

    def wait_for_element_to_be_visible(self, locator_tuple):
        return self.manejadorAccionWeb.wait_for_element_to_be_visible(*locator_tuple)

    def wait_for_element_to_be_present(self, locator_tuple):
        return self.manejadorAccionWeb.wait_for_element_to_be_present(*locator_tuple)


