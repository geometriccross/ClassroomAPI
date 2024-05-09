from __future__ import annotations
from typing import List, Dict, Callable
from enum import Enum
from re import search

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

import pyperclip

def wait_for_element(driver: webdriver, by: By, value: str, timeout: int = 10) -> WebElement:
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
    except TimeoutException:
        print(f"Error: Timeout waiting for element by {by} with value {value}")
        return None

def wait_for_elements(driver: webdriver, by: By, value: str, timeout: int = 10) -> List[WebElement]:
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((by, value)))
    except TimeoutException:
        print(f"Error: Timeout waiting for element by {by} with value {value}")
        return None

# googleアカウントにログインするための情報を扱うための型
class Credentials:
    def __init__(self, email: str, name: str, password: str) -> None:
        self.email = email
        self.name = name
        self.password = password

def login_to_google_classroom(driver: webdriver, cred: Credentials) -> WebDriver:
    """
    Googleアカウントのユーザー名とパスワードを使用して、Google Classroomにログインします。
    """
    
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

def login_collage(driver: webdriver, username: str, password: str) -> WebDriver:
    """大学アカウントにログインを要求された場合"""
    
    if username_input := wait_for_element(driver, By.XPATH, "//input[@id='j_username']"):
        username_input.send_keys(username)
        
    if password_input := wait_for_element(driver, By.XPATH, "//input[@id='j_password']"):
        password_input.send_keys(password)
        
    if submit_button := wait_for_element(driver, By.XPATH, "//button[@type='submit']"):
        submit_button.click()
    
    return driver

def sections(driver: webdriver.Chrome, timeout: float=10) -> Dict[str, str]:
    """
    Google Classroomのセクション名とURLを取得します。
    
    :param driver: WebDriverのインスタンス
    :param timeout: 要素を待つ最大時間
    :return: セクション名をキー、URLを値とする辞書
    """
    
    key_elements = wait_for_elements(
        driver=driver, 
        by=By.XPATH, 
        value="//div[@class='YVvGBb z3vRcc-ZoZQ1']",
        timeout=timeout
    )
    
    url_elements = wait_for_elements(
        driver=driver, 
        by=By.XPATH, 
        value="//a[@class='onkcGd ZmqAt Vx8Sxd']",
        timeout=timeout
    )
    
    if key_elements is None or url_elements is None:
        raise ValueError("Error: Unable to locate keys or URLs.")
    
    keys = [key.text for key in key_elements]
    urls = [url.get_attribute("href") for url in url_elements]
        
    if len(keys) == len(urls):
        return dict(zip(keys, urls))
    else:
        raise ValueError("Error: The number of keys and urls do not match.")

def courses(driver: webdriver.Chrome, timeout: float=10) -> Dict[str, str]:
    """
    Google Classroomのコース名とURLを取得します。

    :param driver: WebDriverのインスタンス
    :param timeout: 要素を待つ最大時間
    :return: コース名をキー、URLを値とする辞書
    """
    option_button_elements = wait_for_elements(
        driver=driver,
        by=By.XPATH,
        value='//div[@jscontroller="bkcTxe"]',
        timeout=timeout
    ) #最初の要素は「クラスへの連絡事項を入力」のため、スキップする
    
    keys = [
        elem.text for elem in wait_for_elements(
            driver=driver,
            by=By.XPATH,
            value='//div[@jsmodel="PTCFbe"]',
            timeout=timeout
        )
    ]
    
    urls = []
    for option_button in option_button_elements:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(option_button))
        option_button.click()

        #リンクをコピーのボタンをクリック
        copy_link_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="JPdR6b hVNH5c qjTEB"]'))
        )
        copy_link_button.click()
        # 'リンクをコピー'ボタンが消失するまで待機
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element(copy_link_button)
        )
        
        # クリップボードにURLがコピーされるのを待機
        WebDriverWait(driver, timeout).until(lambda _: pyperclip.paste() != '')
        urls.append(pyperclip.paste())


    if len(keys) == len(urls):
        return dict(zip(keys, urls))

def files(driver: webdriver.Chrome, timeout: float=10) -> Dict[str, str]:
    elements = wait_for_elements(
        driver=driver,
        by=By.XPATH,
        value='//div[@class="t2wIBc"]',
        timeout=timeout
    )
    
    keys, urls = [], []
    for element in elements:
        keys.append(element.text)
        urls.append(
            element.find_element(By.TAG_NAME, "a").get_attribute("href")
        )
    
    if len(keys) == len(urls):
        return dict(zip(keys, urls))
    else:
        raise ValueError("Error: The number of keys and urls do not match.")

class DriverState(Enum):
    """
    WebDriverの状態を表す列挙型
    """
    PRE_SECTION = 0
    PRE_COURSE = 1
    PRE_FILE = 2

class WhereIsDriver:
    def __init__(self, driver: WebDriver) -> None:
        self.__driver = driver
        super().__init__()
    
    def of(url: str) -> DriverState:
        """
        渡されたdriverのurlを判断し、状態を返します。
        """

        if search("/.../$|/$", url): return DriverState.PRE_SECTION
        elif search("/.{16}$", url): return DriverState.PRE_COURSE
        elif search("/.{16}/details$", url): return DriverState.PRE_FILE

    def is_correct(self, function: Callable[[WebDriver], Dict[str, str]]) -> bool:
        current_state = WhereIsDriver.of(self.__driver.current_url)
    
        return \
            current_state is DriverState.PRE_SECTION and function is sections or \
            current_state is DriverState.PRE_COURSE and function is courses or \
            current_state is DriverState.PRE_FILE and function is files
    
    def try_execute(self, function: Callable[[WebDriver], Dict[str, str]]) -> Dict[str, str] | None:
        if self.is_correct(function):
            return function(self.__driver)