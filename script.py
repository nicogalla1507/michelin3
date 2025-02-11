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
        #chrome_options.add_argument("headless")  
        
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def obtener_url(self):
        print("[INFO] Abriendo página...")
        self.driver.get(self.url)
        time.sleep(3)
        self.ventana_principal = self.driver.current_window_handle  
        print("[INFO] Página cargada correctamente.")

    def fabricantes(self):
        try:
            elemento = self.driver.find_element(By.CLASS_NAME,"ts__step__cta")
            elemento.click()
            time.sleep(3)
            print("[INFO] PESTAÑA (FABRICANTES) ABIERTA")
            
            lista_fabricantes = self.driver.find_element(By.CLASS_NAME,"ts__step__dropdown")
            links = lista_fabricantes.find_elements(By.CLASS_NAME,"ds__link")
            for link in links:
                try:
                    time.sleep(5)
                    print("[INFO] ABRIENDO NUEVA VENTANA ESPERANDO...")
                    print(f"[INFO] ABRIENDO {link.text} ")
                    href = link.get_attribute("href")
                    self.driver.execute_script(f"window.open('{href}', '_blank');")
                    self.version()
                except NoSuchElementException as e:
                    print("[ERROR ELEMENTO] OCURRIO UN ERROR AL ENCONTRAR ELEMENTOS ",e)
        except Exception as e:
            time.sleep(5)
            print("[ERROR] OCURRIO UN PROBLEMA GENERAL",e)
            pass
    
    def version(self):
        lista_versiones = self.driver.find_element(By.CLASS_NAME,"ts__step__dropdown")
        links = lista_versiones.find_elements(By.CLASS_NAME,"ds__link")
        for link in links:
            try:
                time.sleep(3)
                print(f"[INFO] ABRIENDO {link.text} ")
                href = link.get_attribute("href")
                self.driver.execute_script(f"window.open('{href}', '_blank');")
            except NoSuchElementException as e:
                print("[ERROR] OCURRIO UN ERROR AL LISTAR LAS VERSIONES ",e)
            raise NoSuchElementException("ERROR AL INTENTAR ACCEDER A ",link.text)


url_base = "https://www.michelin.cl/auto/browse-tyres/by-vehicle"
script = Script1(url=url_base)

script.iniciar_selenium()
script.obtener_url()
script.fabricantes()
