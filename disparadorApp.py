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
from RabbitMQ.consumidor_basico import consumidor
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
        self.__elemento_caixa_digita_numero_sem_whatsapp = (
            '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]'
        )
        self.elemento_enviar_imagem = (
            '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div/div/span/div/ul/div/div[2]/li/div/input'
        )
        self.elemento_anexar = (
            '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div/div/div'
        )
        self.elemento_clica_imagem = (
            '//span[@data-icon="send"]'
        )
        self.actions = ActionChains(self.driver)
        self.driver.implicitly_wait(20)
        self.wait_long = WebDriverWait(self.driver, 60)
        self.wait_curta = WebDriverWait(self.driver, 3)
        self.__primeiro_acesso_app = True

    def __clica_icone_digita_numero(self) -> None:
        icone = self.driver.find_element(By.XPATH, self.icone_digita_numero)
        icone.click()
        return None

    def __exclui_9_telefone(self, numero: str) -> str:
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

    def __abre_caixa_digita_telefone(self) -> None:
        if self.__primeiro_acesso_app:
            self.__clica_icone_digita_numero()
            self.primeiro_acesso_app = False
        else:
            self.actions.key_down(Keys.CONTROL).key_down(
                Keys.ALT).send_keys('s').key_up(Keys.ALT).key_up(
                    Keys.CONTROL
                ).perform()
        return None

    def __espera_elemento_XPATH(self, elemento: str) -> None:
        self.wait_curta.until(EC.presence_of_element_located((
            By.XPATH, elemento
        )))
        return None

    def __captura_elemento_XPATH(self, elemento: str) -> None:
        return self.driver.find_element(By.XPATH, elemento)

    def whatsappWeb(self):
        self.driver.get("https://web.whatsapp.com/")

    def espera_login(self):
        self.wait_long.until(EC.presence_of_element_located((
            By.XPATH,
            self.elemento_espera_depois_login
        )))
        return self

    def digita_numero_telefone(self, numero: str) -> None:
        ''' Digita o número de telefone via plugin WA Web Plus'''
        self.__abre_caixa_digita_telefone()
        caixa_digita_numero = self.driver.find_element(
            By.XPATH, self.caixa_digita_numero_celular
        )
        caixa_digita_numero.send_keys(self.__exclui_9_telefone(numero))
        sleep(0.5)
        caixa_digita_numero.send_keys(Keys.ENTER)
        return self

    def envia_mensagem(self, mensagem: str) -> None:
        self.__espera_elemento_XPATH(
            self.elemento_caixa_digita_mensagem,
        )
        caixa_digita_mensagem = self.__captura_elemento_XPATH(
            self.elemento_caixa_digita_mensagem
        )
        caixa_digita_mensagem.send_keys(mensagem)
        caixa_digita_mensagem.send_keys(Keys.ENTER)
        sleep(0.3)
        return self
        # # Falta implentar exeção de mensagem sem whatsapp

    def envia_imagem(self, imagem, inscricao=0, nome='', numero=0, cidade='') -> None:
        # try:
        #     self.__espera_elemento_XPATH(
        #         self.__elemento_caixa_digita_numero_sem_whatsapp,
        #     )
        #     self.actions.send_keys(Keys.ESCAPE).send_keys(Keys.ESCAPE).perform()
        #     # Falta implentar registro de número sem whatsapp
        #     return None
        # except:
        self.__espera_elemento_XPATH(
            self.elemento_anexar,
        )
        botao_anexar = self.__captura_elemento_XPATH(self.elemento_anexar)
        botao_anexar.click()
        sleep(2)
        self.__espera_elemento_XPATH(
            self.elemento_enviar_imagem,
        )
        envia_imagem = self.__captura_elemento_XPATH(
            self.elemento_enviar_imagem
        )
        envia_imagem.send_keys(imagem)
        sleep(2)
        self.__espera_elemento_XPATH(
            self.elemento_clica_imagem,
        )
        botao_envia_image = self.__captura_elemento_XPATH(
            self.elemento_clica_imagem
        )
        botao_envia_image.click()
        sleep(2)
        return self
        # Falta implentar registro de mensagem enviada com imagem


if __name__ == "__main__":
    imagem = "/home/rafael/Projetos/Python/disparador_whatsapp/Publicidade_imagem/promocao_cesta_basica.png"
    Wp = DisparadorApp()
    Wp.whatsappWeb()
    Wp.espera_login()
    # ativador = True
    # while ativador is not False:
    #     json_str = consumidor()
    #     print(json_str)
    #     if json_str is None:
    #         sleep(5)
    #         break
    #     else:
    #         corpo = json.loads(json_str)
    #         cliente = corpo["Cliente"]
    #         numero = corpo["numero"]
    #         Wp.digita_numero_telefone(str(numero)).envia_mensagem(f'outro teste {str(cliente)}')
    #         sleep(5)
    Wp.digita_numero_telefone('77992129494').envia_imagem(imagem)
    Wp.driver.quit()
