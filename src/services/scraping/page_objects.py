from __future__ import annotations

from re import search
from typing import Callable, Dict

from pyperclip import paste
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .base import wait_for_elements


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


class Page:
    def __init__(self, driver: WebDriver, timeout: float = 10.0) -> None:
        self.driver: WebDriver = driver
        self.timeout: float = timeout

    @staticmethod
    def id_extract(f) -> Callable[[], Dict[str, str]]:
        """
        この関数は以下の通りの文字列を変換する \n
        ~classroom/u/3/c/NjczNTk2Nzg1MTA0 to NjczNTk2Nzg1MTA0 \n
        ~classroom/u/3/c/NjczNTk2Nzg1MTA0/m/NjczNTk2Nzg1MTI4/details to NjczNTk2Nzg1MTI4
        """

        def __wrapper(*args, **kwargs) -> Dict[str, str]:

            result = {}
            for k, v in f(*args, **kwargs).items():
                pattern = (
                    p if (p := search(".{16}/details$", v)) is not None else search("/.{16}$", v)
                )

                id = None
                if pattern := search(".{16}/details$", v):
                    id = pattern.group().split("/")[0]
                    result[k] = id
                elif pattern := search("/.{16}$", v):
                    id = pattern.group().replace("/", "")
                    result[k] = id
                else:
                    result[k] = ""

            return result

        return __wrapper

    # wrapper functions
    @id_extract
    def sections(self) -> Dict[str, str]:
        """
        Google Classroomのセクション名とURLを取得します。
        """
        return sections(self.driver, self.timeout)

    @id_extract
    def courses(self) -> Dict[str, str]:
        """
        Google Classroomのコース名とURLを取得します。
        """
        return courses(self.driver, self.timeout)

    @id_extract
    def files(self) -> Dict[str, str]:
        return files(self.driver, self.timeout)
