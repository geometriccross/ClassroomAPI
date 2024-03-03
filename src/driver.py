from typing import *
from pathlib import PurePath

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

username = str
password = str

def create_webdriver(driver_path: PurePath, driver_arguments: List[str]):
    # Chromeのドライバーサービスを作成
    service = Service(driver_path)

    # ブラウザの設定
    options = webdriver.ChromeOptions()
    
    for arg in driver_arguments:
        options.add_argument(arg)

    # ブラウザを開く
    return webdriver.Chrome(service=service, options=options)

def login_to_google_classroom(driver: webdriver, username: username, password: password):
    # Google Classroomのログインページに移動
    driver.get("https://classroom.google.com/u/0/h")

    # ログインフォームを探す
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "identifierId"))
    )
    username_input.send_keys(username)
    username_input.send_keys(Keys.RETURN)

    # パスワード入力
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )

    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    # ログイン後のページが読み込まれるまで待機
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "xF2V0d"))
    )

    # ログインしたドライバーを返す
    return driver