import re
import time
import json

from fake_useragent import UserAgent

from seleniumwire import webdriver


from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import CONFIG
from xpaths import XPATHS

class SKusdt:
    def __init__(self) -> None:
        self.ua = UserAgent()


    def get_element(self, driver, XPATH: str):
        return driver.find_element(
            by=By.XPATH,
            value=XPATH,
        )

    def wait_and_find_element(self, driver, XPATH: str, timeout=100):
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    XPATH,
                )
            )
        )

        return driver.find_element(
            by=By.XPATH,
            value=XPATH,
        )

    def create_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument(
            "--no-first-run --no-service-autorun --password-store=basic"
        )

        ua = self.ua.random
        # change user agent
        options.add_argument(f'user-agent={ua}')
        print(ua)

        driver = webdriver.Chrome(options=options)

        return driver
    

    def login(self, user: str, password: str):
        self.driver = self.create_driver()
        self.driver.get('https://my-user-agent.com/')
        input('Press any key to continue...')
        self.driver.get('https://skusdt.com/#/pages/login/login')

        self.wait_and_find_element(
            self.driver,
            XPATHS.USER_INPUT,
        ).send_keys(user)
        
        self.wait_and_find_element(
            self.driver,
            XPATHS.PASSWORD_INPUT,
        ).send_keys(password)
        
        # start catching requests here to get login body request

        time.sleep(3)
        

        self.wait_and_find_element(
            self.driver,
            XPATHS.LOGIN_BUTTON,
        ).click()

        time.sleep(1)

        # print all requests captured
        for request in self.driver.requests:
            if request.response:
                if request.url.startswith('https://skusdt.com/api/app/login?sign='):
                    payload = request.body.decode('utf-8')
                    payload = json.loads(payload)
                    deviceNo = payload['DeviceNo']
                    # get sign from url
                    sign = re.search(r'sign=(.*)', request.url).group(1)
                    print(sign)
                    print(deviceNo)


        input('Press any key to continue...')


if __name__ == '__main__':
    skusdt = SKusdt()
    skusdt.login('vubaoduy101@gmail.com', '123456')