import os
from pathlib import PurePath
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from selenium import webdriver

from . import driver

app = FastAPI()

# グローバルなドライバーを作成
driver: webdriver = None

# アプリケーションの起動時にドライバーを作成
@app.on_event("startup")
async def startup_event():
    global driver
    driver = driver.create_webdriver(
        driver_path = os.getenv("APPDATA").joinpath("chromedriver").as_posix(),
        driver_arguments = ["--headless"]
    )

# ファイルを取得してダウンロードするエンドポイント
@app.get("/download_file")
def download_file(xpath: str, save_path: str):
    """
    指定されたXPathの要素からファイルを取得し、指定されたパスに保存してダウンロードします。

    Parameters:
    - xpath: str: ダウンロードするファイルのXPath
    - save_path: str: ダウンロードしたファイルを保存するパス

    Returns:
    - FileResponse: ダウンロードしたファイルのレスポンス
    """
    global driver
    try:
        # ファイルを取得
        driver.get_file(driver, xpath, save_path)
        
        # ダウンロードが成功したファイルを返す
        return FileResponse(save_path, media_type="application/octet-stream", filename=os.path.basename(save_path))
    except Exception as e:
        # エラーメッセージを返す
        raise HTTPException(status_code=500, detail=f"ファイルのダウンロードに失敗しました: {e}")

# アプリケーションの終了時にドライバーを終了
@app.on_event("shutdown")
async def shutdown_event():
    global driver
    if driver is not None:
        driver.quit()
