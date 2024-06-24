from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .base import wait_for_element
from .literals import LOGIN_URL


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

    driver.get(LOGIN_URL)

    if email_input := wait_for_element(driver, By.XPATH, "//input[@type='email']"):
        email_input.send_keys(cred.email)
        wait_for_element(driver, By.ID, "identifierNext").click()

    if WebDriverWait(driver, 10).until(EC.url_contains("shibboleth")):
        login_collage(driver, cred.name, cred.password)

    if next_button := wait_for_element(driver, By.XPATH, "//div[@jsname='Njthtb']"):
        next_button.click()

    # パスワードを要求されたりされなかったりするため
    if WebDriverWait(driver, 5).until(EC.url_contains("accounts.google.com")):
        return driver
    else:
        if password_input := wait_for_element(
            driver,
            By.CSS_SELECTOR,
            "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input",
        ):
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
