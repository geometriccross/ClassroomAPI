import os
from pathlib import Path
from time import time
from fastapi import FastAPI, HTTPException, status
from selenium import webdriver
from shutil import rmtree

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
@app.get("/add_driver", status_code=status.HTTP_201_CREATED)
async def add_driver():
    global drivers
    drivers.append(instance_gen.__next__())
    return {"message": "new driver is added"}

@app.delete("/remove_driver/{driver_index}", status_code=status.HTTP_200_OK)
async def remove_driver(driver_index: int):
    global drivers
    try:
        driver_to_remove = drivers.pop(driver_index)
        driver_to_remove.quit()
        rmtree(driver_to_remove.capabilities['chrome']['userDataDir'])
        return {"message": f"Driver at index {driver_index} has been removed"}
    except IndexError:
        raise HTTPException(status_code=404, detail=f"No driver found at index {driver_index}")

@app.delete("/clear_driver", status_code=status.HTTP_204_NO_CONTENT)
async def clear_driver():
    global drivers
    if len(drivers) > 0:
        for driver in drivers:
            driver.quit()
            rmtree(driver.capabilities['chrome']['userDataDir'])
        drivers.clear()
    else:
        raise HTTPException(status_code=404, detail="No driver to clear")

# アプリケーションの終了時にドライバーを終了
@app.on_event("shutdown")
async def shutdown_event():
    global drivers
    for driver in drivers:
        driver.quit()
