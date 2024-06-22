from __future__ import annotations

from enum import Enum
from re import search
from typing import Callable, Dict

from pyperclip import paste
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .base import wait_for_elements
from .permission_passing import login_to_google_classroom


def sections(driver: WebDriver, timeout: float = 10) -> Dict[str, str]:
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
        timeout=timeout,
    )

    url_elements = wait_for_elements(
        driver=driver,
        by=By.XPATH,
        value="//a[@class='onkcGd ZmqAt Vx8Sxd']",
        timeout=timeout,
    )

    if key_elements is None or url_elements is None:
        raise ValueError("Error: Unable to locate keys or URLs.")

    keys: list = [key.text for key in key_elements]
    urls: list = [url.get_attribute("href") for url in url_elements]

    if len(keys) == len(urls):
        return dict(zip(keys, urls))
    else:
        raise ValueError("Error: The number of keys and urls do not match.")


def courses(driver: WebDriver, timeout: float = 10) -> Dict[str, str]:
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
        timeout=timeout,
    )  # 最初の要素は「クラスへの連絡事項を入力」のため、スキップする

    keys = [
        elem.text
        for elem in wait_for_elements(
            driver=driver,
            by=By.XPATH,
            value='//div[@jsmodel="PTCFbe"]',
            timeout=timeout,
        )
    ]

    urls = []
    for option_button in option_button_elements:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(option_button))
        option_button.click()

        # リンクをコピーのボタンをクリック
        copy_link_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="JPdR6b hVNH5c qjTEB"]'))
        )
        copy_link_button.click()
        # 'リンクをコピー'ボタンが消失するまで待機
        WebDriverWait(driver, timeout).until(EC.invisibility_of_element(copy_link_button))

        # クリップボードにURLがコピーされるのを待機
        WebDriverWait(driver, timeout).until(lambda _: paste() != "")
        urls.append(paste())

    if len(keys) == len(urls):
        return dict(zip(keys, urls))
    else:
        raise ValueError("Error: The number of keys and urls do not match.")


def files(driver: WebDriver, timeout: float = 10) -> Dict[str, str]:
    elements = wait_for_elements(
        driver=driver, by=By.XPATH, value='//div[@class="t2wIBc"]', timeout=timeout
    )

    keys, urls = [], []
    for element in elements:
        keys.append(element.text)
        urls.append(element.find_element(By.TAG_NAME, "a").get_attribute("href"))

    if len(keys) == len(urls):
        return dict(zip(keys, urls))
    else:
        raise ValueError("Error: The number of keys and urls do not match.")


class DriverState(Enum):
    """
    WebDriverの状態を表す列挙型
    """

    OUT_CONTROL = -1
    PRE_SECTION = 0
    PRE_COURSE = 1
    PRE_FILE = 2
    NOT_LOGINED = 3


class WhereIsDriver:
    def __init__(self, driver: WebDriver) -> None:
        self.__driver = driver
        super().__init__()

    @staticmethod
    def of(url: str) -> DriverState:
        """
        渡されたdriverのurlを判断し、状態を返します。
        """

        if search("/.../$|/$", url):
            return DriverState.PRE_SECTION
        elif search("/.{16}$", url):
            return DriverState.PRE_COURSE
        elif search("/.{16}/details$", url):
            return DriverState.PRE_FILE
        elif search("data:,", url):
            return DriverState.NOT_LOGINED
        else:
            return DriverState.OUT_CONTROL

    def is_correct(self, function: Callable[[WebDriver], Dict[str, str]]) -> bool:
        current_state = WhereIsDriver.of(self.__driver.current_url)

        return (
            current_state is DriverState.PRE_SECTION
            and function is sections
            or current_state is DriverState.PRE_COURSE
            and function is courses
            or current_state is DriverState.PRE_FILE
            and function is files
            or current_state is DriverState.NOT_LOGINED
            and function is login_to_google_classroom
        )

    def try_execute(self, function: Callable[[WebDriver], Dict[str, str]]) -> Dict[str, str] | None:
        if self.is_correct(function):
            return function(self.__driver)
        else:
            return None
