import os
from pathlib import Path
import shutil
import pytest
from dotenv import load_dotenv

from selenium.webdriver.chrome.webdriver import WebDriver

from src.driver import generate_driver_instances
from src import scraping

load_dotenv(".env")

# 環境変数からログイン情報を取得
USER_NAME = os.getenv("COLLAGE_USERNAME")
USER_EMAIL = os.getenv("COLLAGE_EMAIL")
PASSWORD = os.getenv("COLLAGE_PASSWORD")

@pytest.fixture
def test_driver() -> WebDriver:
    test_dir = Path("test/chrome_drivers")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    driver_generator = generate_driver_instances(test_dir, [])
    driver = next(driver_generator)
    yield driver
    
    driver.quit()
    shutil.rmtree(test_dir)

def test_login_to_google_classroom(test_driver):
    test_driver.get("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fclassroom.google.com&ifkv=ARZ0qKK0GsFwI5PXniQdLUuY_N4_bgWD6xGS9M02CmscmVL7nKgDlaGJRNeJV-QAmwwvP1r-fQ2muA&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S319460678%3A1711092114297087&theme=mn&ddm=0")
    scraping.login_to_google_classroom(test_driver, USER_EMAIL, USER_NAME, PASSWORD)
    assert test_driver is not None

def test_sections(test_driver):
    # Google Classroomにログインしていることを前提とする
    test_login_to_google_classroom(test_driver)
    
    # Google Classroomのセクション（クラス）一覧ページに移動
    test_driver.get("https://classroom.google.com/u/0/h")
    
    # セクション（クラス）の要素を取得
    sections = scraping.sections(test_driver, 10)
    
    # セクション（クラス）が少なくとも1つ以上存在することを確認
    assert len(sections) > 0, "セクションが存在しません。"
    for section_name, section_url in sections.items():
        assert section_name is not None
        assert section_url is not None

def test_courses(test_driver):
    test_login_to_google_classroom(test_driver)
    sections = scraping.sections(test_driver, 10)
    
    #sectionから最初の要素を取得
    section = list(sections.keys())[0]
    test_driver.get(sections[section])
    
    courses = scraping.courses(test_driver, 10)
    assert len(courses) > 0, "コースが存在しません。"
    for course_name, course_url in courses.items():
        assert course_name is not None
        assert course_url is not None