from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options


class DisparadorApp:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.options = Options()
        self.options.add_argument("--user-data-dir=./Cookies")
        self.driver = webdriver.Chrome(
            options=self.options,
            service=ChromeService(ChromeDriverManager().install())
        )
        self.driver.get("https://web.whatsapp.com/")
        self.elemento_espera_depois_login = (
            '//*[@id="app"]/div/div/div[4]/header/div[1]/div/img'
        )
        self.wait = WebDriverWait(self.driver, 60)
