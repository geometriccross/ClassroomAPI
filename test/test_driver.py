import os
import pytest
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
from src.driver import login_to_google_classroom

def test_login_to_google_classroom():
    load_dotenv()
    FOR_TEST_USERNAME = os.environ["FOR_TEST_USERNAME"]
    FOR_TEST_EMAIL = os.environ["FOR_TEST_EMAIL"]
    FOR_TEST_PASSWORD = os.environ["FOR_TEST_PASSWORD"]
    
    try:
        driver = webdriver.Chrome()
        login_to_google_classroom(driver, FOR_TEST_EMAIL, FOR_TEST_PASSWORD)
    except TimeoutException:
        assert False, "TimeoutException occurred during login"