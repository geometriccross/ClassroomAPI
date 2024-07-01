from re import search
from sqlite3 import Cursor
from typing import Dict

from selenium.webdriver.remote.webdriver import WebDriver

from .scraper import courses, files, sections


class Page:
    def __init__(self, driver: WebDriver, timeout: float = 10.0) -> None:
        self.driver: WebDriver = driver
        self.timeout: float = timeout

    @staticmethod
    def id_extract(url: str) -> str:
        """
        この関数は以下の通りの文字列を変換する \n
        ~classroom/u/3/c/NjczNTk2Nzg1MTA0 to NjczNTk2Nzg1MTA0 \n
        ~classroom/u/3/c/NjczNTk2Nzg1MTA0/m/NjczNTk2Nzg1MTI4/details to NjczNTk2Nzg1MTI4
        """

        if pattern := search(".{16}/details$", url):
            return pattern.group().split("/")[0]
        elif pattern := search("/.{16}$", url):
            return pattern.group().replace("/", "")
        else:
            return ""

    # wrapper functions
    def sections(self, cursor: Cursor) -> None:
        """
        Google Classroomのセクション名とURLを取得します。
        """
        for url in sections(self.driver, self.timeout).values():
            id = Page.id_extract(url)
            if id == "":
                raise ValueError(f"Error: Invalid id: {id}")

            cursor.execute(f"INSERT INTO sections VALUES {id}")

    def courses(self) -> Dict[str, str]:
        """
        Google Classroomのコース名とURLを取得します。
        """
        return courses(self.driver, self.timeout)

    def files(self) -> Dict[str, str]:
        return files(self.driver, self.timeout)
