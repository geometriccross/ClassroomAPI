from typing import List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .base import wait_for_element


# googleアカウントにログインするための情報を扱うための型
class Credentials:
    def __init__(self, email: str, name: str, password: str) -> None:
        self.email = email
        self.name = name
        self.password = password

def login_to_google_classroom(driver: WebDriver, cred: Credentials) -> WebDriver:
    """
    Googleアカウントのユーザー名とパスワードを使用して、Google Classroomにログインします。
    """
    
    driver.get("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fclassroom.google.com&ifkv=ARZ0qKK0GsFwI5PXniQdLUuY_N4_bgWD6xGS9M02CmscmVL7nKgDlaGJRNeJV-QAmwwvP1r-fQ2muA&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S319460678%3A1711092114297087&theme=mn&ddm=0")
    
    if email_input := wait_for_element(driver, By.XPATH, "//input[@type='email']"):
        email_input.send_keys(cred.email)
        wait_for_element(driver, By.ID, "identifierNext").click()
    
    if WebDriverWait(driver, 10).until(EC.url_contains("shibboleth")):
        login_collage(driver, cred.name, cred.password)

    if next_button := wait_for_element(driver, By.XPATH, "//div[@jsname='Njthtb']"):
            next_button.click()

    if password_input := wait_for_element(driver, By.CSS_SELECTOR, "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input"):
        password_input.send_keys(cred.password)
        wait_for_element(driver, By.ID, "passwordNext").click()

    return driver

def login_collage(driver: WebDriver, username: str, password: str) -> WebDriver:
    """大学アカウントにログインを要求された場合"""
    
    if username_input := wait_for_element(driver, By.XPATH, "//input[@id='j_username']"):
        username_input.send_keys(username)
        
    if password_input := wait_for_element(driver, By.XPATH, "//input[@id='j_password']"):
        password_input.send_keys(password)
        
    if submit_button := wait_for_element(driver, By.XPATH, "//button[@type='submit']"):
        submit_button.click()
    
    return driver