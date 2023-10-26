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
