import json
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


class BootResposta():
    def __init__(self):
        self.bolinha_notificacao = 'aumms1qt'
        self.__elemento_espera_depois_login = (
            '//*[@id="app"]/div/div/div[4]/header/div[1]/div/img'
        )
        self.__elemento_numero_telefone = (
            '//*[@id="main"]/header/div[2]/div/div/div/span'
        )
        self.driver = webdriver.Chrome()
        self.options = Options()
        self.options.add_argument("--user-data-dir=./Cookies")
        self.driver = webdriver.Chrome(
            options=self.options,
            service=ChromeService(ChromeDriverManager().install())
        )
        self.driver.implicitly_wait(20)
        self.wait = WebDriverWait(self.driver, 60)

    def espera_login(self):
        '''
        Método espera login do whatsappweb
        '''
        self.wait.until(EC.presence_of_element_located((
            By.XPATH,
            self.__elemento_espera_depois_login
        )))
        return self

    def clica_bolinha(self):
        '''
        Método encontra bolinha de notificação de nova mensagem e clica
        um pouco a esquerda evitando a seta de menu da bolinha.
        '''
        notificacao = self.driver.find_elements(
        By.CLASS_NAME, self.bolinha_notificacao
        )
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(
            notificacao[-1], 0, -20
        ).click().perform()

    def captura_numero_telefopne(self):
        '''
        Método captura número de telefone
        '''
        elemento_telefone = self.driver.find_element(
            By.XPATH, self.__elemento_numero_telefone
        )
        return elemento_telefone.text


if __name__ == '__main__':
    boot = BootResposta()
    boot.driver.get("https://web.whatsapp.com/")
    boot.espera_login()
    boot.clica_bolinha()
    sleep(2)
    numero = boot.captura_numero_telefopne()
    print(numero)
    sleep(3)
