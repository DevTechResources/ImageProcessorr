import unittest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ImageProcessorTests (unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usag<e')
        options.add_argument('--window-size=1920,1080')
        
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 15)
       
        cls.BASE_URL = "http://localhost:5173"
        cls.API_URL = "http://localhost:5000"
        
        cls.TEST_IMAGE_DIR = os.path.join(os.getcwd, 'test_image')
        os.makedirs(cls.TEST_IMAGE_DIR, exist_ok=True)
        return super().setUpClass()
     
    def setUp(self):
        """Configuración antes de cada test"""
        self.driver.get(self.BASE_URL)
        time.sleep(2)
        
    def  take_screenshot(self, name):
        """Capturar screenshot para debugging"""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"screenshot_{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"Screenshot guardado: {filename}")

    def test_01_landing_page_loads(self):
        """Verificar que la landing page carga correctamente"""
        try:
            self.assertIn("ImageProcessor", self.driver.title)
            
            logo = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".logo-image"
            )
            self.assertTrue(logo.is_displayed())
            
            cta_button = self.driver.find_element(By.CSS_SELECTOR, ".cta-butt"
            self.assertTrue(cta_button.is_displayed())
            
            print(" Landing page carga correctamente")
        except Exception as e:
            self.take_screenshot("landing_page_error")
            self.fail(f"Error en landing page: {str(e)}")
            )
            
    def test_02_navigation_menu(self):
        """Verificar navegación entre páginas"""
        try:
        procesador_btn = self.wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text
        )
        procesador_btn.cllick()
        time.sleep(2)
        
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text
        )
                                                           
        ayuda_btn = self.driver.find_element(By.XPATH, "//button[contains
            ayuda_btn_click()
            time.sleep(2)
            self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text
        )
        print("✓ Navegación funciona correctamente")
        except Exception as e:
            self.take_screenshot("navigation_error")
            self.fail(f"Error en navegación: {str(e)}")