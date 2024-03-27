from typing import List
from collections.abc import Generator
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

def webdriver_profile_generator(prefix: Path) -> Generator[Path, None, None]:
    """
    Chromeのプロファイルディレクトリを生成するジェネレーター関数

    Args:
        prefix (Path): ChromeDriverプロファイルのルートとするパス

    Yields:
        Path: 新しく作成されたプロファイルディレクトリのパス
    """

    profile_index = 0
    while True:
        profile_path = Path(prefix).joinpath(f"profile_{profile_index}")
        yield Path(profile_path)
        profile_index += 1

def create_webdriver(profile_dir: Path, driver_arguments: List[str]) -> Generator[WebDriver, None, None]:
    """
    新しいChromeドライバーのインスタンスを作成する

    Args:
        profile_dir (Path): ChromeDriverプロファイルのルートディレクトリ
        driver_arguments (List[str]): ChromeDriverに渡す引数のリスト

    Yields:
        WebDriver: 新しく作成されたChromeドライバーのインスタンス
    """
    
    profile_generator = webdriver_profile_generator(profile_dir)
    
    while True:
        profile_path = next(profile_generator)
        profile_path.mkdir(exist_ok=True)
    
        service = Service()
        options = Options()
        options.add_argument(f"--user-data-dir={profile_path.absolute()}")

        for arg in driver_arguments:
            options.add_argument(arg)
    
        yield webdriver.Chrome(service=service, options=options)