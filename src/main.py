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
instance_gen = driver.generate_driver_instances(
    profile_dir = Path(os.getenv("APPDATA")).joinpath("classroomAPI/chromedrivers"),
    driver_arguments = ["--headless"]
)

# アプリケーションの起動時にドライバーを作成
@app.on_event("startup")
async def startup_event():
    global drivers
    global instance_gen
    drivers.append(instance_gen.__next__())

@app.get("/list")
async def list():
    return {"working webdriver": drivers.__str__()}

# アプリケーションの終了時にドライバーを終了
@app.on_event("shutdown")
async def shutdown_event():
    global drivers
    for driver in drivers:
        driver.quit()
