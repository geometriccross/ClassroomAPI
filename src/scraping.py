from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

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

def login_to_google_classroom(driver: webdriver, user_email: str, user_name: str, password: str) -> WebDriver:
    """
    Google Takeoutにアクセスしてログインします。
    Googleアカウントのユーザー名とパスワードを使用して、Google Takeoutにログインします。
    """
    
    if email_input := wait_for_element(driver, By.XPATH, "//input[@type='email']"):
        email_input.send_keys(user_email)
        wait_for_element(driver, By.ID, "identifierNext").click()
    
    if WebDriverWait(driver, 10).until(EC.url_contains("shibboleth")):
        login_collage(driver, user_name, password)

    if next_button := wait_for_element(driver, By.XPATH, "//div[@jsname='Njthtb']"):
            next_button.click()

    if password_input := wait_for_element(driver, By.CSS_SELECTOR, "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input"):
        password_input.send_keys(password)
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

def sections(driver: webdriver.Chrome, timeout: float) -> Dict[str, str]:
    """
    Google Classroomのセクション名とURLを取得します。
    
    :param driver: WebDriverのインスタンス
    :param timeout: 要素を待つ最大時間
    :return: セクション名をキー、URLを値とする辞書
    """
    driver.get("https://classroom.google.com/u/0/h")
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

def courses(driver: webdriver.Chrome, timeout: float) -> Dict[str, str]:
    elements = wait_for_element(
        driver=driver,
        by=By.XPATH,
        value='//div[@class="t2wIBc"]',
        timeout=timeout
    )
    
    if elements is None:
        raise ValueError("Error: Unable to locate elements.")
    
    course_info = {}
    for element in elements:
        key = element.text
        url = element.get_attribute("href")
        course_info[key] = url
    
    return course_info