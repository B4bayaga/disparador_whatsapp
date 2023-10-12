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
        self.elemento_espera_depois_login = (
            '//*[@id="app"]/div/div/div[4]/header/div[1]/div/img'
        )
        self.caixa_digita_numero_celular = (
            '/html/body/div[4]/div[1]/div/input'
        )
        self.icone_digita_numero = (
            '//*[@id="startNonContactChat"]/div/span'
        )
        self.elemento_caixa_digita_mensagem = (
            '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]'
        )
        self.actions = ActionChains(self.driver)
        self.driver.implicitly_wait(20)
        self.wait = WebDriverWait(self.driver, 60)
        self.__primeiro_acesso_app = True

    def whatsappWeb(self):
        self.driver.get("https://web.whatsapp.com/")

    def __clica_icone_digita_numero(self):
        icone = self.driver.find_element(By.XPATH, self.icone_digita_numero)
        icone.click()

    def __exclui_9_telefone(self, numero):
        '''
        Exclui o número 9 depois nos telefones que tem menos de 10 digitos
        '''
        if len(numero) == 11:
            if numero[0] == '1' and numero[1] == '1':
                return numero
            elif numero[2] == '9':
                return numero[:2] + numero[3:]
        else:
            return numero

    def __abre_caixa_digita_telefone(self):
        if self.__primeiro_acesso_app:
            self.__clica_icone_digita_numero()
            self.primeiro_acesso_app = False
        else:
            self.actions.key_down(Keys.CONTROL).key_down(
                Keys.ALT).send_keys('s').key_up(Keys.ALT).key_up(
                    Keys.CONTROL
                ).perform()

    def espera_login(self):
        self.wait.until(EC.presence_of_element_located((
            By.XPATH,
            self.elemento_espera_depois_login
        )))
        return self

    def digita_numero_telefone(self, numero):
        ''' Digita o número de telefone via plugin WA Web Plus'''
        self.__abre_caixa_digita_telefone()
        caixa_digita_numero = self.driver.find_element(
            By.XPATH, self.caixa_digita_numero_celular
        )
        caixa_digita_numero.send_keys(self.__exclui_9_telefone(numero))
        sleep(0.5)
        caixa_digita_numero.send_keys(Keys.ENTER)
        return self

    def envia_mensagem(self, mensagem):
        self.wait.until(EC.presence_of_element_located((
            By.XPATH, self.elemento_caixa_digita_mensagem
        )))
        caixa_digita_mensagem = self.driver.find_element(
            By.XPATH, self.elemento_caixa_digita_mensagem
        )
        caixa_digita_mensagem.send_keys(mensagem)
        caixa_digita_mensagem.send_keys(Keys.ENTER)
        return self

    def envia_imagem(self, imagem):
        pass


if __name__ == "__main__":
    Wp = DisparadorApp()
    Wp.whatsappWeb()
    Wp.espera_login()
    Wp.digita_numero_telefone('77992129494').envia_mensagem('outro teste')
    sleep(500)
