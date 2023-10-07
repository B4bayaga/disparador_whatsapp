from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from datetime import datetime, timedelta
from time import sleep


class DisparadorWP:
    ''' Disparador de mensagens de cobrança via Whatsapp'''
    def __init__(self) -> None:
        self.mensagem = None
        self.dias_vencimento = 0
        self.botao_enviar = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]'
        self.caixa_digita_numero_celular = '/html/body/div[4]/div[1]/div/input'
        self.caixa_texto_envia_mensagem = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]'
        self.elemento_espera1 = '//*[@id="app"]/div/div/div[4]/header/div[1]/div/img'
        self.elemento_espera2 = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]'
        self.elemento_espera3 = '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]'
        self.elemento_anexar = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div/div/div'
        self.elemento_enviar_imagem = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div/div/span/div/ul/div/div[2]/li/div/input'
        self.elemento_clica_imagem = '//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div'
        self.filiais = ["anage", "barra_do_choca", "belo_campo", "caraibas", "divisopolis", "encruzilhada", "itambe", "piripa", "planalto", "ribeirao_do_largo", "tremedal", "vitoria_da_conquista"]
        self.imagem_cesta_basica = r'C:\Projetos\Boot\Producao\Boot-producao\Publicidade_imagem\promocao_cesta_basica.png'
        self.imagem_gas = r'C:\Projetos\Boot\Producao\Boot-producao\Publicidade_imagem\promocao_gas.jpeg'
        self.image = False
        self.hoje = datetime.now().date()
        self.options = Options()
        self.options.add_argument("--user-data-dir=C:\\Projetos\Boot\\Producao\\Boot-producao\\Chrome_Cooki_Dev")
        self.driver = webdriver.Chrome(options=self.options, service=ChromeService(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 300)
        self.wait_2 = WebDriverWait(self.driver, 10)
        self.actions = ActionChains(self.driver)

    def registra_envio_mensagem(self, inscricao, nome, fone, enviado: bool, filial) -> None:
        inscricao= int(inscricao)
        nome= str(nome)
        fone= int(fone)
        enviado= enviado
        filial= str(filial)
        vsql = f"INSERT INTO mensagens (insc, nome, fone, enviado, filial) VALUES('{inscricao}', '{nome}', '{fone}', '{enviado}', '{filial}')"
        injectMensagemEnviada(vsql)

    def mensagem_cobranca_texto(self, inscricao, nome) -> str:
        ''' Metodo criando mensagem de cobrança'''
        return (f"{inscricao} - Olá Sr.(a) {nome} tudo bem?! {self.mensagem}")

    def mensagem_cobranca_imagem(self, imagem) -> None:
        self.wait_2.until(EC.presence_of_element_located((By.XPATH, self.elemento_anexar)))
        botao_anexar = self.driver.find_element(By.XPATH, self.elemento_anexar)
        botao_anexar.click()
        sleep(2)
        self.wait_2.until(EC.presence_of_element_located((By.XPATH, self.elemento_enviar_imagem)))
        envia_imagem = self.driver.find_element(By.XPATH, self.elemento_enviar_imagem)
        envia_imagem.send_keys(imagem)
        self.wait_2.until(EC.presence_of_element_located((By.XPATH,self.elemento_clica_imagem)))
        botao_envia_image = self.driver.find_element(By.XPATH, self.elemento_clica_imagem)
        botao_envia_image.click()
    
    def exclui_9_telefone(self, numero):
        ''' Exclui o número 9 depois do DDD nos telefones que tem menos de 10 digitos'''
        if len(numero) == 11:
            if numero[2] == '9':
                return numero[:2] + numero[3:]
        else:
            return numero
        
    def transforma_string_para_data(self, data) -> datetime:
        ''' Metodo transforma string para data'''
        return datetime.strptime(data, '%d/%m/%Y')

    def subtrai_dias(self, dias) -> datetime:
        ''' Metodo subtrai dias'''
        return self.hoje - timedelta(days=dias)

    def filtra_vencimento(self, lista, dias) -> list:
        ''' Metodo filtra vencimento'''
        lista_ = []
        vencimento = self.subtrai_dias(dias)
        for i in lista:
            vencimento1 = self.transforma_string_para_data(i[5])
            if vencimento1.date() == vencimento:
                lista_.append(i)
        return lista_

    def digita_numero_telefone(self, numero):
        ''' Digita o número de telefone via plugin WA Web Plus'''
        self.actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys('s').key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
        try:
            self.wait_2.until(EC.presence_of_element_located((By.XPATH, self.caixa_digita_numero_celular)))
        except:
            self.actions.send_keys(Keys.ESCAPE).send_keys(Keys.ESCAPE).perform()
            return None
        caixa_digita_numero = self.driver.find_element(By.XPATH, self.caixa_digita_numero_celular)
        caixa_digita_numero.send_keys(self.exclui_9_telefone(numero))
        sleep(1)
        caixa_digita_numero.send_keys(Keys.ENTER)

    def envia_mensagem(self, inscricao, nome, numero, cidade) -> None:
        sleep(3)
        self.digita_numero_telefone(numero)
        sleep(2)
        try:
            self.wait_2.until(EC.presence_of_element_located((By.XPATH, self.elemento_espera3)))
            self.registra_envio_mensagem(inscricao=inscricao, nome=nome, fone=numero, enviado=False, filial=cidade)
            self.actions.send_keys(Keys.ESCAPE).send_keys(Keys.ESCAPE).perform()
            return self
        except Exception as ex:
            self.wait_2.until(EC.presence_of_element_located((By.XPATH, self.caixa_texto_envia_mensagem)))
            caixa_texto_envia_mensagem = self.driver.find_element(By.XPATH, self.caixa_texto_envia_mensagem)
            sleep(1)
            caixa_texto_envia_mensagem.click()
            caixa_texto_envia_mensagem.send_keys(self.mensagem_cobranca_texto(inscricao, nome))
            sleep(1)
            botao_enviar = self.driver.find_element(By.XPATH, self.botao_enviar)
            self.registra_envio_mensagem(inscricao=inscricao, nome=nome, fone=numero, enviado=True, filial=cidade)
            botao_enviar.click()
            sleep(random.randint(20, 35))
            return None

    def envia_mensagem_imagem(self, image, inscricao, nome, numero, cidade) -> None:
        sleep(3)
        self.digita_numero_telefone(numero)
        sleep(2)
        try:
            self.wait_2.until(EC.presence_of_element_located((By.XPATH, self.elemento_espera3)))
            print(inscricao, nome, numero, cidade)
            print(type(inscricao), type(nome), type(numero), type(cidade))
            self.registra_envio_mensagem(inscricao=inscricao, nome=nome, fone=numero, enviado=False, filial=cidade)
            self.actions.send_keys(Keys.ESCAPE).send_keys(Keys.ESCAPE).perform()
            return None
        except Exception as ex:
            sleep(2)
            caixa_texto_envia_mensagem = self.driver.find_element(By.XPATH, self.caixa_texto_envia_mensagem)
            sleep(1)
            self.mensagem_cobranca_imagem(image)
            self.registra_envio_mensagem(inscricao=inscricao, nome=nome, fone=numero, enviado=True, filial=cidade)
            sleep(random.randint(20, 35))
            return self

    def clientes_2023(self, fone_2 = False) -> None:
        ''' Gera e dispara Mensagens de Cobrança para clientes cadastrados depois de 2023'''
        if fone_2 == False:
            for filial in self.filiais:
                clientes = gera_cob_planos_2023_fone_1(filial)
                cobranca = self.filtra_vencimento(clientes, self.dias_vencimento)
                print(*cobranca)
                for cliente in cobranca:
                    if self.image == False :
                        self.envia_mensagem(str(cliente[0]), str(cliente[1]), str(cliente[2]), filial)
                        sleep(1)
                    elif self.image == True and filial == self.filiais[11]:
                        self.envia_mensagem_imagem(self.imagem_gas, str(cliente[0]), str(cliente[1]), str(cliente[2]), filial)
                    elif self.image == True:
                        self.envia_mensagem_imagem(self.imagem_cesta_basica, str(cliente[0]), str(cliente[1]), str(cliente[2]), filial)
        elif fone_2 == True:
            for filial in self.filiais:
                clientes = gera_cob_planos_2023_fone_2(filial)
                cobranca = self.filtra_vencimento(clientes, self.dias_vencimento)
                print(*cobranca)
                for cliente in cobranca:
                    if self.image == False :
                        self.envia_mensagem(str(cliente[0]), str(cliente[1]), str(cliente[2]), filial, str(cliente[5]))
                        sleep(1)
                    elif self.image == True and filial == self.filiais[11]:
                        self.envia_mensagem_imagem(self.imagem_gas, str(cliente[0]), str(cliente[1]), str(cliente[2]), filial, str(cliente[5]))
                    elif self.image == True:
                        self.envia_mensagem_imagem(self.imagem_cesta_basica, str(cliente[0]), str(cliente[1]), str(cliente[2]), filial, str(cliente[5]))
        return self

    def clientes_em_debito(self, fone_2 = False) -> None:
        ''' Gera e dispara Mensagens de Cobrança para clientes em debito'''
        if fone_2 == False:
            for filial in self.filiais:
                clientes = gera_cob_planos_fone_1(filial)
                cobranca = self.filtra_vencimento(clientes, self.dias_vencimento)
                print(*cobranca)
                for cliente in cobranca:
                    if self.image == False :
                        self.envia_mensagem(str(cliente[0]), str(cliente[1]), str(cliente[2]), filial)
                        sleep(1)
                    elif self.image == True and filial == self.filiais[11]:
                        self.envia_mensagem_imagem(self.imagem_gas, str(cliente[0]), str(cliente[1]), str(cliente[2]), filial)
                    elif self.image == True:
                        self.envia_mensagem_imagem(self.imagem_cesta_basica, str(cliente[0]), str(cliente[1]), str(cliente[2]), filial)
        elif fone_2 == True:
            for filial in self.filiais:
                clientes = gera_cob_planos_fone_2(filial)
                cobranca = self.filtra_vencimento(clientes, self.dias_vencimento)
                print(*cobranca)
                for cliente in cobranca:
                    if self.image == False :
                        self.envia_mensagem(str(cliente[0]), str(cliente[1]), str(cliente[2]), filial)
                        sleep(1)
                    elif self.image == True and filial == self.filiais[11]:
                        self.envia_mensagem_imagem(self.imagem_gas, str(cliente[0]), str(cliente[1]), str(cliente[2]), filial)
                    elif self.image == True:
                        self.envia_mensagem_imagem(self.imagem_cesta_basica, str(cliente[0]), str(cliente[1]), str(cliente[2]), filial)
        return self

if __name__ == '__main__':
    wp = DisparadorWP()
    wp.image = True
    wp.dias_vencimento
    wp.mensagem = "Passando para lembrar que a mensalidade do seu plano com a Pax Nacional falta confirmação, o pagamento pode ser feito na rede bancaria e casas lotéricas de todo país, também temos a opção de debito automático via cartão de crédito. Tenha um ótimo dia!!!"
    wp.driver.get('https://web.whatsapp.com/')
    wp.wait.until(EC.presence_of_element_located((By.XPATH, wp.elemento_espera1)))
    sleep(5)
    wp.clientes_em_debito()
    wp.driver.close()

