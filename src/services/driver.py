from __future__ import annotations

from pathlib import Path
from shutil import rmtree
from threading import Thread
from typing import Generator, List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

from .scraping.permission_passing import Credentials, login_to_google_classroom


def webdriver_profile_generator(
    prefix: Path, default_index: int = 0
) -> Generator[Path, None, None]:
    """
    Generates Chrome profile directories.

    Args:
        prefix (Path): The root path for ChromeDriver profiles.
        default_index (int, optional):
            The default index for the profile directory.

    Yields:
        Path: The path of the newly created profile directory.
    """
    profile_index = default_index
    while True:
        profile_path = Path(prefix).joinpath(f"profile_{profile_index}")
        yield Path(profile_path)
        profile_index += 1


def generate_driver_instances(
    profile_gen: Generator[Path, None, None],
    driver_arguments: List[str],
    cred: Credentials,
) -> Generator[WebDriver, None, None]:
    """
    新しいChromeドライバーのインスタンスを作成する

    Args:
        profile_dir (Path): ChromeDriverプロファイルのルートディレクトリ
        driver_arguments (List[str]): ChromeDriverに渡す引数のリスト
        cred (Credentials): Google Classroomにログインするためのアカウント情報

    Yields:
        WebDriver: 新しく作成されたChromeドライバーのインスタンス
    """

    while True:
        profile_path = next(profile_gen)
        profile_path.mkdir(exist_ok=True)

        service = Service()
        options = Options()
        options.add_argument(f"--user-data-dir={profile_path.absolute()}")

        if len(driver_arguments) > 0:
            for arg in driver_arguments:
                options.add_argument(arg)

        driver = webdriver.Chrome(service=service, options=options)
        login_to_google_classroom(driver, cred)
        yield driver


class StoredDrivers(List):
    """
    Chromeドライバーのインスタンスを保存するシングルトンクラス
    """

    def __init__(self, profile_dir: Path, driver_args: List[str], cred: Credentials) -> None:
        super().__init__()
        self.__profile_dir = profile_dir
        self.__driver_arguments = driver_args
        self.__cred = cred
        self.__instance_gen = generate_driver_instances(
            webdriver_profile_generator(self.__profile_dir),
            driver_arguments=self.__driver_arguments,
            cred=self.__cred,
        )

        self.grow()

    def __new__(cls, **kwag) -> StoredDrivers:
        if not hasattr(cls, "__instance") or getattr(cls, "__instance") is None:
            cls.__instance = super().__new__(cls)
            for k, v in kwag.items():
                setattr(cls.__instance, k, v)

            return cls.__instance
        else:
            return cls.__instance

    def grow(self) -> None:
        """
        新しいdriverを、内部に保存されているgeneratorから追加する
        """
        driver = next(self.__instance_gen)
        self.append(driver)

    def shrink(self) -> None:
        """
        driverを末端から削除する
        """
        if len(self) < 1:
            return
        else:
            driver = self.pop()
            driver.quit()
            rmtree(driver.capabilities["chrome"]["userDataDir"])
            self.__instance_gen = generate_driver_instances(
                webdriver_profile_generator(self.__profile_dir, len(self)),
                self.__driver_arguments,
                self.__cred,
            )

    def clear(self) -> None:
        threads: List[Thread] = []
        for driver in self:
            quite_t = Thread(target=driver.quit)
            rmtree_t = Thread(
                target=rmtree,
                args=(driver.capabilities["chrome"]["userDataDir"],),
            )

            threads.append(quite_t)
            threads.append(rmtree_t)

            quite_t.start()
            rmtree_t.start()

        for thread in threads:
            thread.join()

        return super().clear()
