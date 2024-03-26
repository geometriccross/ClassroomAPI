import os
from pathlib import Path
from time import time
import pytest
from dotenv import load_dotenv

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from src.driver import create_webdriver
from src.scraping import wait_for_elements, login_to_google_classroom, login_collage, sections, courses

load_dotenv(".env")

# 環境変数からログイン情報を取得
USER_NAME = os.getenv("COLLAGE_USERNAME")
USER_EMAIL = os.getenv("COLLAGE_EMAIL")
PASSWORD = os.getenv("COLLAGE_PASSWORD")

@pytest.fixture
def test_driver() -> WebDriver:
    driver_path = Path(os.getenv("APPDATA")).joinpath("classroomAPI/chromedrivers/test").joinpath(hash(time()).__str__())
    
    yield create_webdriver(
        driver_path=driver_path,
        driver_arguments=[]
    )
    
    driver_path.unlink()

def test_login_to_google_classroom(test_driver):
    test_driver.get("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fclassroom.google.com&ifkv=ARZ0qKK0GsFwI5PXniQdLUuY_N4_bgWD6xGS9M02CmscmVL7nKgDlaGJRNeJV-QAmwwvP1r-fQ2muA&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S319460678%3A1711092114297087&theme=mn&ddm=0")
    login_to_google_classroom(test_driver, USER_EMAIL, USER_NAME, PASSWORD)
    assert test_driver is not None

def test_sections(mocker):
    driver_mock = mocker.MagicMock()
    mocker.patch('ClassroomAPI.src.scraping.wait_for_element', side_effect=[None, None])
    # ログイン情報を環境変数から取得して使用
    driver = login_to_google_classroom(driver_mock, USER_NAME, PASSWORD)
    with pytest.raises(ValueError):
        sections(driver, 10)

def test_courses(mocker):
    driver_mock = mocker.MagicMock()
    element_mock = MagicMock(spec=WebElement)
    element_mock.text = "Course 1"
    element_mock.get_attribute.return_value = "http://example.com"
    mocker.patch('ClassroomAPI.src.scraping.wait_for_element', return_value=[element_mock])
    # ログイン情報を環境変数から取得して使用
    driver = login_to_google_classroom(driver_mock, USER_NAME, PASSWORD)
    result = courses(driver, 10)
    assert result == {"Course 1": "http://example.com"}