import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("https://web.whatsapp.com/")
    yield driver
    driver.quit()


def test_abrindo_pagia_whatsapp_web(driver):
    assert driver.title == "WhatsApp"
