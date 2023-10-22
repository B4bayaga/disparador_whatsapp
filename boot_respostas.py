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


class BootResposta():
    def __init__(self):
        self.bolinha_notificacao = 'aumms1qt'
        self.driver = webdriver.Chrome()
        self.options = Options()
        self.options.add_argument("--user-data-dir=./Cookies")
        self.driver = webdriver.Chrome(
            options=self.options,
            service=ChromeService(ChromeDriverManager().install())
        )
        self.driver.implicitly_wait(20)
        self.wait = WebDriverWait(self.driver, 60)


boot = BootResposta()
boot.driver.get("https://web.whatsapp.com/")
notificacao = boot.driver.find_elements(
    By.CLASS_NAME, boot.bolinha_notificacao
)
print(len(notificacao))
notificacao[-1].click()
sleep(2)
