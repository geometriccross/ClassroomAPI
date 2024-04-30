import os
from pathlib import Path
import shutil
import pytest
from dotenv import load_dotenv

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.driver import generate_driver_instances
from src import scraping
from typing import Generator, Any

load_dotenv(".env")

# 環境変数からログイン情報を取得
USER_NAME = os.getenv("COLLAGE_USERNAME")
USER_EMAIL = os.getenv("COLLAGE_EMAIL")
PASSWORD = os.getenv("COLLAGE_PASSWORD")

COURSES_TEST_URL = os.getenv("COURSES_TEST_URL")
FILES_TEST_URL = os.getenv("FILES_TEST_URL")

@pytest.fixture
def test_driver() -> Generator[Any, Any, WebDriver]:
    test_dir = Path("test/chrome_drivers")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    driver_generator = generate_driver_instances(test_dir, ["--headless=new"])
    driver = next(driver_generator)
    yield driver
    
    driver.quit()
    shutil.rmtree(test_dir)

def test_login_to_google_classroom(test_driver: WebDriver):
    test_driver.get("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fclassroom.google.com&ifkv=ARZ0qKK0GsFwI5PXniQdLUuY_N4_bgWD6xGS9M02CmscmVL7nKgDlaGJRNeJV-QAmwwvP1r-fQ2muA&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S319460678%3A1711092114297087&theme=mn&ddm=0")
    scraping.login_to_google_classroom(test_driver, USER_EMAIL, USER_NAME, PASSWORD)
    assert test_driver is not None
    
    assert "https://classroom.google.com" in test_driver.current_url

def test_sections(test_driver: WebDriver):
    # Google Classroomにログインしていることを前提とする
    test_login_to_google_classroom(test_driver)
    
    # Google Classroomのセクション（クラス）一覧ページに移動
    test_driver.get("https://classroom.google.com")
    
    # セクション（クラス）の要素を取得
    sections = scraping.sections(test_driver, 10)
    
    # セクション（クラス）が少なくとも1つ以上存在することを確認
    assert len(sections) > 0, "セクションが存在しません。"
    for section_name, section_url in sections.items():
        assert section_name is not None
        assert section_url is not None

def test_courses(test_driver: WebDriver):
    test_driver.get(COURSES_TEST_URL)
    scraping.login_to_google_classroom(test_driver, USER_EMAIL, USER_NAME, PASSWORD)
    
    courses = scraping.courses(test_driver, 10)
    assert len(courses) > 0, "コースが存在しません。"
    for course_name, course_url in courses.items():
        assert course_name is not None
        assert course_url is not None

def test_files(test_driver: WebDriver):
    test_driver.get(FILES_TEST_URL)
    scraping.login_to_google_classroom(test_driver, USER_EMAIL, USER_NAME, PASSWORD)

    files = scraping.files(test_driver, 10)
    assert len(files) > 0, "ファイルが存在しません。"
    for file_name, file_url in files.items():
        assert file_name is not None
        assert file_url is not None