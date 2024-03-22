import os
from pathlib import Path
from time import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from selenium import webdriver

from src import driver

app = FastAPI()

# グローバルなドライバーを作成
drivers: list[webdriver.Chrome] = []

# アプリケーションの起動時にドライバーを作成
@app.on_event("startup")
async def startup_event():
    global drivers
    drivers.append(
        driver.create_webdriver(
            driver_path = Path(os.getenv("APPDATA")).
                            joinpath("classroomAPI/chromedrivers").
                            joinpath(hash(time()).__str__()),
            driver_arguments = ["--headless=new"]
        )
    )

@app.get("/list")
async def list():
    return {"working webdriver": drivers.__str__()}

# アプリケーションの終了時にドライバーを終了
@app.on_event("shutdown")
async def shutdown_event():
    global drivers
    for driver in drivers:
        driver.quit()
