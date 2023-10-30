import pytest
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from boot_respostas import BootResposta


boot = BootResposta()
boot.driver.get("https://web.whatsapp.com/")


def test_confirmando_url_pagina():
    assert boot.driver.current_url == "https://web.whatsapp.com/"


def test_abrindo_pagia_whatsapp_web():
    assert boot.driver.title == "WhatsApp"


def test_espera_login():
    assert boot.espera_login()


def test_verifica_elemento_bolinha_notificacao():
    assert boot.wait.until(EC.presence_of_element_located((
        By.CLASS_NAME,
        boot.bolinha_notificacao
    )))


def test_telefone_apos_clica_bolinha():
    sleep(2)
    boot.clica_bolinha()
    assert boot.wait.until(EC.presence_of_element_located((
        By.XPATH,
        boot._BootResposta__elemento_numero_telefone
    )))


def test_metodo_captura_numero_telefone():
    numero = boot.captura_numero_telefone()
    assert numero


def test_elemento_mensagem_recebidas():
    assert boot.wait.until(EC.presence_of_element_located((
        By.CLASS_NAME,
        boot._BootResposta__elementos_menssagens_recebidas
    )))


def test_elemento_caixa_mensagem():
    assert boot.wait.until(EC.presence_of_element_located((
        By.XPATH,
        boot._BootResposta__elemento_caixa_digita_mensagem
    )))


def test_mensgem_recebida():
    mensagem = boot.ler_mensagens_recebidas()
    assert mensagem


def test_monta_dicionario():
    numero = '77992129494'
    mensagem = 'Oi'
    dicionario = boot.monta_dicionario(numero, mensagem)
    assert type(dicionario) == dict


def test_conteudo_dicionario():
    numero = '77992129494'
    mensagem = 'Oi'
    dicionario = boot.monta_dicionario(numero, mensagem)
    assert dicionario['numero'] == numero
    assert dicionario['mensagem'] == mensagem
