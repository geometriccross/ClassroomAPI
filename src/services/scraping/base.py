from typing import List

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def wait_for_element(driver: WebDriver, by: str, value: str, timeout: float = 10) -> WebElement:
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
    except TimeoutException as e:
        raise ValueError(e, f"Error: Timeout waiting for element by {by} with value {value}")


def wait_for_elements(
    driver: WebDriver, by: str, value: str, timeout: float = 10
) -> List[WebElement]:
    return WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((by, value)))
