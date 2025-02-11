from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

class Script1:
    def __init__(self, url):
        self.url = url 
        self.driver = None
        self.ventana_principal = None  

    def iniciar_selenium(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")  
        chrome_options.add_argument("--no-sandbox")
        #chrome_options.add_argument("--headless")  # Opcional si no quieres abrir ventanas físicas
        
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def obtener_url(self):
        print("[INFO] Abriendo página...")
        self.driver.get(self.url)
        time.sleep(3)
        self.ventana_principal = self.driver.current_window_handle  # Guarda la ventana principal
        print("[INFO] Página cargada correctamente.")

    def fabricantes(self):
        try:
            elemento = self.driver.find_element(By.CLASS_NAME, "ts__step__cta")
            elemento.click()
            time.sleep(3)
            print("[INFO] PESTAÑA (FABRICANTES) ABIERTA")

            lista_fabricantes = self.driver.find_element(By.CLASS_NAME, "ts__step__dropdown")
            links = lista_fabricantes.find_elements(By.CLASS_NAME, "ds__link")

            if links:
                for link in links:
                    try:
                        time.sleep(2)
                        href = link.get_attribute("href")
                        print(f"[INFO] Abriendo {link.text} en nueva pestaña...")
                        
                        self.driver.execute_script("window.open(arguments[0], '_blank');", href)
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        self.version()
                        self.driver.close()
                        self.driver.switch_to.window(self.ventana_principal)
                    except NoSuchElementException as e:
                        print("[ERROR ELEMENTO] Ocurrió un error al encontrar elementos", e)
            else:
                print("[INFO] Solo hay 1 fabricante, procesando en la misma ventana...")
                self.version()
        except Exception as e:
            print("[ERROR] Ocurrió un problema general", e)

    def version(self):
        try:
            lista_versiones = self.driver.find_element(By.CLASS_NAME, "ts__step__dropdown")
            links = lista_versiones.find_elements(By.CLASS_NAME, "ds__link")

            if links:
                for link in links:
                    try:
                        time.sleep(2)
                        href = link.get_attribute("href")
                        print(f"[INFO] Abriendo versión {link.text} en nueva pestaña...")
                        
                        self.driver.execute_script("window.open(arguments[0], '_blank');", href)
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        self.añofabricacion()
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                    except NoSuchElementException as e:
                        print("[ERROR] Ocurrió un error al listar las versiones", e)
            else:
                print("[INFO] Solo hay 1 versión, procesando en la misma ventana...")
                self.añofabricacion()
        except Exception as e:
            print("[ERROR] No se encontraron versiones disponibles:", e)

    def añofabricacion(self):
        try:
            lista_años = self.driver.find_element(By.CLASS_NAME, "ts__step__dropdown")
            links = lista_años.find_elements(By.CLASS_NAME, "ds__link")

            if links:
                for link in links:
                    try:
                        time.sleep(2)
                        href = link.get_attribute("href")
                        print(f"[INFO] Abriendo año {link.text} en nueva pestaña...")
                        
                        self.driver.execute_script("window.open(arguments[0], '_blank');", href)
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        time.sleep(2)
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                    except NoSuchElementException as e:
                        print("[ERROR] Ocurrió un error al listar los años de fabricación", e)
            else:
                print("[INFO] Solo hay 1 año, procesando en la misma ventana...")
        except Exception as e:
            print("[ERROR] No se encontraron años de fabricación disponibles:", e)

# URL de la página objetivo
url_base = "https://www.michelin.cl/auto/browse-tyres/by-vehicle"

# Crear e iniciar el script
script = Script1(url=url_base)
script.iniciar_selenium()
script.obtener_url()
script.fabricantes()
