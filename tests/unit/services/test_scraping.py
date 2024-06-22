import os
import shutil
from pathlib import Path

import pytest
from dotenv import load_dotenv
from selenium.webdriver.chrome.webdriver import WebDriver

from src.services.driver import generate_driver_instances, webdriver_profile_generator
from src.services.scraping import page_objects as po
from src.services.scraping.permission_passing import Credentials

load_dotenv(".env")


def get_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Environment variable {key} is not set.")
    else:
        return value


# 環境変数からログイン情報を取得
credentials = Credentials(
    email=get_env("COLLAGE_USERNAME"),
    name=get_env("COLLAGE_USERNAME"),
    password=get_env("COLLAGE_PASSWORD"),
)

LOGIN_URL = get_env("LOGIN_URL")
SECTION_TEST_URL = get_env("SECTION_TEST_URL")
COURSES_TEST_URL = get_env("COURSES_TEST_URL")
FILES_TEST_URL = get_env("FILES_TEST_URL")


@pytest.fixture
def test_driver():
    test_dir = Path("test/chrome_drivers")
    test_dir.mkdir(parents=True, exist_ok=True)

    driver_generator = generate_driver_instances(
        profile_gen=webdriver_profile_generator(test_dir),
        driver_arguments=["--headless=new"],
        cred=credentials,
    )

    driver = next(driver_generator)
    yield driver

    driver.quit()
    shutil.rmtree(test_dir)


def test_sections(test_driver: WebDriver):
    # Google Classroomのセクション（クラス）一覧ページに移動
    test_driver.get(SECTION_TEST_URL)

    # セクション（クラス）の要素を取得
    sections = po.sections(test_driver, 10)

    # セクション（クラス）が少なくとも1つ以上存在することを確認
    assert len(sections) > 0, "セクションが存在しません。"
    for section_name, section_url in sections.items():
        assert section_name is not None
        assert section_url is not None


def test_courses(test_driver: WebDriver):
    test_driver.get(COURSES_TEST_URL)

    courses = po.courses(test_driver, 10)
    assert len(courses) > 0, "コースが存在しません。"
    for course_name, course_url in courses.items():
        assert course_name is not None
        assert course_url is not None
