from conftest import get_env
from selenium.webdriver.chrome.webdriver import WebDriver

from src.services.scraping.page_objects import Page, courses, sections

SECTION_TEST_URL = get_env("SECTION_TEST_URL")
COURSES_TEST_URL = get_env("COURSES_TEST_URL")
FILES_TEST_URL = get_env("FILES_TEST_URL")


def test_sections(test_driver: WebDriver):
    # Google Classroomのセクション（クラス）一覧ページに移動
    test_driver.get(SECTION_TEST_URL)

    # セクション（クラス）の要素を取得
    sections_value = sections(test_driver, 10)

    # セクション（クラス）が少なくとも1つ以上存在することを確認
    assert len(sections_value) > 0, "セクションが存在しません。"
    for section_name, section_url in sections_value.items():
        assert section_name is not None
        assert section_url is not None


def test_courses(test_driver: WebDriver):
    test_driver.get(COURSES_TEST_URL)

    courses_value = courses(test_driver, 10)
    assert len(courses_value) > 0, "コースが存在しません。"
    for course_name, course_url in courses_value.items():
        assert course_name is not None
        assert course_url is not None


def test_Page_id_extract():
    test_urls = [
        {
            "data": "https://classroom.google.com/u/3/c/NjcyOTEyOTk2Nzgx",
            "expected": "NjcyOTEyOTk2Nzgx",
        },
        {
            "data": "https://classroom.google.com/u/3/c/NjcyOTEyOTk2Nzgx/m/NjkwNTE0Njc3NDA3/details",
            "expected": "NjkwNTE0Njc3NDA3",
        },
        {
            "data": "https://classroom.google.com/u/3/c/NjcyOTEyOTk2Nzgx/m/NjkwNTE0Njc3NDA3/submissions/by-status/all-students/late",
            "expected": "",
        },
    ]

    for param in test_urls:
        data, expected = param.values()
        id = Page.id_extract(lambda: {"data": data})()["data"]
        assert id == expected
