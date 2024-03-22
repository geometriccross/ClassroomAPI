from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

username = str
password = str

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

def login_collage(driver: webdriver, username: str, email: str, password: str):
    """大学アカウントにログインを要求された場合"""
    
    if username_input := wait_for_element(driver, By.XPATH, "//input[@id='j_username']"):
        username_input.send_keys(username)
        
    if password_input := wait_for_element(driver, By.XPATH, "//input[@id='j_password']"):
        password_input.send_keys(password)
        
    if submit_button := wait_for_element(driver, By.XPATH, "//button[@type='submit']"):
        submit_button.click()