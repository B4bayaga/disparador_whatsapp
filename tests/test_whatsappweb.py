import pytest
import string
import random
from time import sleep
from disparadorApp import DisparadorApp
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def random_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


numero_cobranca = '77999255107'
numero_rafael = '77992129494'
@pytest.fixture
def Wp():
    Wp = DisparadorApp()
    Wp.whatsappWeb()
    yield Wp
    Wp.driver.quit()


def test_abrindo_pagia_whatsapp_web(Wp):
    assert Wp.driver.title == "WhatsApp"


def test_confirmando_url_pagina(Wp):
    assert Wp.driver.current_url == "https://web.whatsapp.com/"


def test_elemento_espera_apos_login(Wp):
    assert Wp.espera_login()


@pytest.mark.slow
def test_elemento_digita_numero_whatsapp(Wp):
    Wp.espera_login()
    Wp._DisparadorApp__abre_caixa_digita_telefone()
    assert Wp.wait_curta.until(EC.presence_of_element_located((
        By.XPATH,
        Wp.caixa_digita_numero_celular
    )))


def test_elemento_numero_sem_whatsapp(Wp):
    Wp.espera_login()
    Wp.digita_numero_telefone(numero_cobranca)
    assert Wp.wait_curta.until(EC.presence_of_element_located((
        By.XPATH,
        Wp.caixa_digita_numero_celular
    )))


def test_remove_9_telefone():
    Wp = DisparadorApp()
    assert Wp._DisparadorApp__exclui_9_telefone('11992129494') == '11992129494'
    assert Wp._DisparadorApp__exclui_9_telefone('77992129494') == '7792129494'
    assert Wp._DisparadorApp__exclui_9_telefone('7792129494') == '7792129494'


def test_elemento_espera_caixa_digita_mensagem(Wp):
    Wp.espera_login()
    Wp.digita_numero_telefone(numero_rafael)
    assert Wp.wait_curta.until(EC.presence_of_element_located((
        By.XPATH,
        Wp.elemento_caixa_digita_mensagem
    )))


def test_texto_envia_mensagem(Wp):
    palavra_teste = random_generator()
    Wp.espera_login()
    Wp.digita_numero_telefone(numero_rafael)
    Wp.envia_mensagem(palavra_teste)
    sleep(0.5)
    mensagens_enviada = Wp.driver.find_elements(
        By.XPATH,
        '//span[@dir="ltr"]'
    )
    numero = len(mensagens_enviada)
    assert mensagens_enviada[numero - 1].text == palavra_teste
