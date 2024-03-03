from typing import *
from pathlib import PurePath

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

username = str
password = str

def create_webdriver(driver_path: PurePath, driver_arguments: List[str]):
    # Chromeのドライバーサービスを作成
    service = Service(driver_path)

    # ブラウザの設定
    options = webdriver.ChromeOptions()
    
    for arg in driver_arguments:
        options.add_argument(arg)

    # ブラウザを開く
    return webdriver.Chrome(service=service, options=options)

def wait_for_element(driver: webdriver, by: By, value: str, timeout: int = 10):
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
    except TimeoutException:
        print(f"Error: Timeout waiting for element by {by} with value {value}")
        return None

def login_to_google_classroom(driver: webdriver, username: username, password: password):
    """
    Google Takeoutにアクセスしてログインします。
    Googleアカウントのユーザー名とパスワードを使用して、Google Takeoutにログインします。
    """

    driver.get("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Ftakeout.google.com%2F%3Fhl%3Dja&followup=https%3A%2F%2Ftakeout.google.com%2F%3Fhl%3Dja&hl=ja&ifkv=ATuJsjzLD6xO4Hk_ZGE3sE9VhY6ACjrc0naKIJQ6DUlMF4eTd7LAnFfft-R23r6VqUjo71Wx7IJo4w&osid=1&passive=1209600&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S1728425499%3A1709466484511131&theme=glif")
    
    # ログインフォームを探す
    if username_input := wait_for_element(driver, By.ID, "identifierId"):
        username_input.send_keys(username)
        wait_for_element(driver, By.ID, "identifierNext").click()
    
    # パスワード入力
    if password_input := wait_for_element(driver, By.CSS_SELECTOR, "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input"):
        password_input.send_keys(password)
        wait_for_element(driver, By.ID, "passwordNext").click()

    if easy_to_login := wait_for_element(driver, By.XPATH, "//div[@jsname='eBSUOb']", 2):
        easy_to_login.click()

    return driver