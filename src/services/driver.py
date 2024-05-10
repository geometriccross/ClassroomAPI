from threading import Thread
from typing import List
from shutil import rmtree
from collections.abc import Generator
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

from typing import Generator
from pathlib import Path

def webdriver_profile_generator(prefix: Path, default_index: int = 0) -> Generator[Path, None, None]:
    """
    Generates Chrome profile directories.

    Args:
        prefix (Path): The root path for ChromeDriver profiles.
        default_index (int, optional): The default index for the profile directory. Defaults to 0.

    Yields:
        Path: The path of the newly created profile directory.
    """
    profile_index = default_index
    while True:
        profile_path = Path(prefix).joinpath(f"profile_{profile_index}")
        yield Path(profile_path)
        profile_index += 1

def generate_driver_instances(profile_gen: Generator[Path, None, None], driver_arguments: List[str]) -> Generator[WebDriver, None, None]:
    """
    新しいChromeドライバーのインスタンスを作成する

    Args:
        profile_dir (Path): ChromeDriverプロファイルのルートディレクトリ
        driver_arguments (List[str]): ChromeDriverに渡す引数のリスト

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
    
        yield webdriver.Chrome(service=service, options=options)

class StoredDrivers(List):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    
    def __init__(self, profile_dir: Path, driver_arguments: List[str]) -> None:
        super().__init__()
        self.__profile_dir = profile_dir
        self.__driver_arguments = driver_arguments
        self.__instance_gen = generate_driver_instances(
            webdriver_profile_generator(self.__profile_dir),
            driver_arguments = driver_arguments
        )
        
        self.append(
            self.__instance_gen.__next__()
        )
    
    def __del__(self) -> None:
        for _ in range(len(self)):
            self.shrink()
    
    def grow(self) -> None:
        """
        新しいdriverを、内部に保存されているgeneratorから追加する
        """
        self.append(
            self.__instance_gen.__next__()
        )
    
    def shrink(self) -> None:
        """
        driverを末端から削除する
        """
        if len(self) < 1:
            return
        else:
            driver = self.pop()
            driver.quit()
            rmtree(driver.capabilities['chrome']['userDataDir'])
            self.__instance_gen = generate_driver_instances(
                webdriver_profile_generator(self.__profile_dir, len(self)),
                self.__driver_arguments
            )