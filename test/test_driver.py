import pytest
from pytest_mock import MockerFixture
import shutil
from pathlib import Path
from selenium.webdriver.chrome.webdriver import WebDriver

from src.services import driver

TEST_DIR = Path("test/chrome_drivers")

@pytest.fixture(scope="module")
def setup_teardown():
    # テストの前処理
    test_dir = TEST_DIR
    test_dir.mkdir(parents=True, exist_ok=True)

    yield

    # テストの後処理
    shutil.rmtree(test_dir)

def test_webdriver_profile_generator():
    profile_generator = driver.webdriver_profile_generator("")
    assert next(profile_generator) == Path("profile_0")
    assert next(profile_generator) == Path("profile_1")
    
    profile_generator = driver.webdriver_profile_generator("", 5)
    assert next(profile_generator) == Path("profile_5")

def test_stored_drivers_shrink(setup_teardown, mocker: MockerFixture):
    drivers = driver.StoredDrivers(profile_dir=TEST_DIR, driver_arguments=["--headless=new"])
    assert len(drivers) == 1
    
    drivers.shrink()
    assert len(drivers) == 0
    
    #異常を起こさないか確認
    drivers.shrink()
    
    ins_index = 3
    for _ in range(ins_index):
        drivers.grow()
    
    assert len(drivers) == ins_index
    drivers.shrink()
    ins_index -= 1
    
    assert TEST_DIR.joinpath(f"profile_{ins_index-1}").exists()
    drivers.grow()
    ins_index += 1
    
    assert TEST_DIR.joinpath(f"profile_{ins_index-1}").exists()