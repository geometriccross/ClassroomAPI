import os
import pytest
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
from src.driver import *

def test_login_to_google_classroom():
    load_dotenv()
    FOR_TEST_USERNAME = os.environ["FOR_TEST_USERNAME"]
    FOR_TEST_EMAIL = os.environ["FOR_TEST_EMAIL"]
    FOR_TEST_PASSWORD = os.environ["FOR_TEST_PASSWORD"]
    
    try:
        driver = webdriver.Chrome()
        driver.get("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Ftakeout.google.com%2F%3Fhl%3Dja&followup=https%3A%2F%2Ftakeout.google.com%2F%3Fhl%3Dja&hl=ja&ifkv=ATuJsjzLD6xO4Hk_ZGE3sE9VhY6ACjrc0naKIJQ6DUlMF4eTd7LAnFfft-R23r6VqUjo71Wx7IJo4w&osid=1&passive=1209600&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S1728425499%3A1709466484511131&theme=glif")
        login_to_google_classroom(driver, FOR_TEST_EMAIL, FOR_TEST_PASSWORD)
    except TimeoutException:
        assert False, "TimeoutException occurred during login"

def test_login_collage():
    load_dotenv()
    COLLAGE_PORTAL_SITE = os.environ["COLLAGE_PORTAL_SITE"]
    COLLAGE_USERNAME = os.environ["COLLAGE_USERNAME"]
    COLLAGE_EMAIL = os.environ["COLLAGE_EMAIL"]
    COLLAGE_PASSWORD = os.environ["COLLAGE_PASSWORD"]

    try:
        driver = webdriver.Chrome()
        driver.get(COLLAGE_PORTAL_SITE)
        if login_button := wait_for_element(driver, By.CSS_SELECTOR, "#left_container > div > div > div > a"):
            login_button.click()

        login_collage(driver, COLLAGE_USERNAME, COLLAGE_EMAIL, COLLAGE_PASSWORD)
    except TimeoutException:
        assert False, "TimeoutException occurred during login"
