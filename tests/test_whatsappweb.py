import pytest
from disparadorApp import DisparadorApp
from disparadorApp import DisparadorApp
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


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
    assert Wp.wait.until(EC.presence_of_element_located((
        By.XPATH, Wp.elemento_espera_depois_login
    )))


def test_elemento_digita_numero_whatsapp(Wp):
    Wp.wait.until(EC.presence_of_element_located((
        By.XPATH, Wp.elemento_espera_depois_login
    )))
    Wp._DisparadorApp__abre_caixa_digita_telefone()
    assert Wp.wait.until(EC.presence_of_element_located((
        By.XPATH, Wp.caixa_digita_numero_celular
    )))


def test_remove_9_telefone():
    Wp = DisparadorApp()
    assert Wp._DisparadorApp__exclui_9_telefone('11992129494') == '11992129494'
    assert Wp._DisparadorApp__exclui_9_telefone('77992129494') == '7792129494'
    assert Wp._DisparadorApp__exclui_9_telefone('7792129494') == '7792129494'


def test_elemento_espera_caixa_digita_mensagem(Wp):
    Wp.wait.until(EC.presence_of_element_located((
        By.XPATH, Wp.elemento_espera_depois_login
    )))
    Wp.digita_numero_telefone('77992129494')
    assert Wp.wait.until(EC.presence_of_element_located((
        By.XPATH, Wp.elemento_caixa_digita_mensagem
    )))


def test_texto_envia_mensagem(Wp):
    pass
