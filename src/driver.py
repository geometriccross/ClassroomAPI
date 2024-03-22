from typing import *
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def create_webdriver(driver_path: Path, driver_arguments: List[str]):
    service = Service(driver_path
        if driver_path.exists()
        else driver_path.mkdir(parents=True, exist_ok=True)
    )

    options = webdriver.ChromeOptions()
    
    #headlessなどのオプションを追加
    for arg in driver_arguments:
        options.add_argument(arg)

    return webdriver.Chrome(service=service, options=options)