from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep


class DisparadorApp:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.options = Options()
        self.options.add_argument("--user-data-dir=./Cookies")
        self.driver = webdriver.Chrome(
            options=self.options,
            service=ChromeService(ChromeDriverManager().install())
        )
        self.driver.get("https://web.whatsapp.com/")
        self.elemento_espera_depois_login = (
            '//*[@id="app"]/div/div/div[4]/header/div[1]/div/img'
        )
        self.caixa_digita_numero_celular = (
            '/html/body/div[4]/div[1]/div/input'
        )
        self.actions = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 60)

    def __exclui_9_telefone(self, numero):
        return numero
    
    def __abre_caixa_digita_telefone(self):
         self.actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('s').key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
       

    def digita_numero_telefone(self, numero):
        ''' Digita o número de telefone via plugin WA Web Plus'''
        self.__abre_caixa_digita_telefone()
        # breakpoint()
        try:
            self.wait_2.until(EC.presence_of_element_located((By.XPATH, self.caixa_digita_numero_celular)))
        except:
            self.actions.send_keys(Keys.ESCAPE).send_keys(Keys.ESCAPE).perform()
            return None
        caixa_digita_numero = self.driver.find_element(By.XPATH, self.caixa_digita_numero_celular)
        caixa_digita_numero.send_keys(self.__exclui_9_telefone(numero))
        sleep(1)
        caixa_digita_numero.send_keys(Keys.ENTER)


Wp = DisparadorApp()
Wp.digita_numero_telefone("77992129494")
