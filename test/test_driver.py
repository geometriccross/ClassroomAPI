import unittest
from unittest.mock import MagicMock, patch

from selenium import webdriver

from src.driver import login_to_google_classroom

class TestLoginToGoogleClassroom(unittest.TestCase):
    def test_login_to_google_classroom(self):
        driver = webdriver.Chrome()
        login_to_google_classroom(driver, 'test_username', 'test_password')

if __name__ == '__main__':
    unittest.main()