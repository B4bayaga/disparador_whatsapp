import pytest
from disparadorApp import DisparadorApp
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def Wp():
    Wp = DisparadorApp()
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
