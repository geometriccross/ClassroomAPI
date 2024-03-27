import pytest
import shutil
from pathlib import Path
from selenium.webdriver.chrome.webdriver import WebDriver

from src.driver import *

@pytest.fixture(scope="module")
def setup_teardown():
    # テストの前処理
    test_dir = Path("test/chrome_drivers")
    test_dir.mkdir(parents=True, exist_ok=True)

    yield

    # テストの後処理
    shutil.rmtree(test_dir)

def test_webdriver_profile_generator():
    profile_generator = webdriver_profile_generator("")
    profile = next(profile_generator)
    assert profile == Path("profile_0")
    profile = next(profile_generator)
    assert profile == Path("profile_1")

def test_create_webdriver(setup_teardown):
    # テストケース1: 実際にドライバのインスタンスを作成できることを確認する
    driver_generator = create_webdriver(Path("test/chrome_drivers"), ["--headless"])
    driver = next(driver_generator)
    assert isinstance(driver, WebDriver)
    driver.quit()

    # テストケース2: 複数回ジェネレータがnextで呼ばれた際に新しいインスタンスを作成できることを確認する
    driver1 = next(driver_generator)
    driver2 = next(driver_generator)
    assert isinstance(driver1, WebDriver)
    assert isinstance(driver2, WebDriver)
    assert driver1.session_id != driver2.session_id
    driver1.quit()
    driver2.quit()