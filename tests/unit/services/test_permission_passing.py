import shutil
from pathlib import Path
from time import time

from conftest import get_env
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.services.scraping.permission_passing import (
    Credentials,
    login_to_google_classroom,
)

LOGIN_URL = get_env("LOGIN_URL")


def test_login(cred: Credentials):
    TEST_DIR = Path("tests/chrome_drivers")
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)

    random_dir = TEST_DIR.joinpath(str(hash(time())))

    options = Options()
    options.add_argument("--headless=new")

    try:
        driver = webdriver.Chrome(options=options)
        login_to_google_classroom(driver, cred)
    finally:
        if random_dir.exists():
            shutil.rmtree(random_dir)
