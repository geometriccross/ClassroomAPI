import os
from shutil import rmtree
from fastapi import APIRouter, HTTPException, status
from src.services.driver import *

driver_router = APIRouter()

# グローバルなドライバーを作成
drivers: list[WebDriver] = []
instance_gen = generate_driver_instances(
    profile_dir = Path(os.getenv("APPDATA")).joinpath("classroomAPI/chromedrivers"),
    driver_arguments = ["--headless=new"]
)

@driver_router.get("/list")
async def list():
    return {
        "working webdriver": 
            [driver.session_id for driver in drivers]
        }

@driver_router.get("/add_driver", status_code=status.HTTP_201_CREATED)
async def add_driver():
    global drivers
    drivers.append(instance_gen.__next__())
    return {"message": "new driver is added"}

@driver_router.delete("/remove_driver/{driver_index}", status_code=status.HTTP_200_OK)
async def remove_driver(driver_index: int):
    global drivers
    try:
        driver_to_remove = drivers.pop(driver_index)
        driver_to_remove.quit()
        rmtree(driver_to_remove.capabilities['chrome']['userDataDir'])
        return {"message": f"Driver at index {driver_index} has been removed"}
    except IndexError:
        raise HTTPException(status_code=404, detail=f"No driver found at index {driver_index}")

@driver_router.delete("/clear_driver", status_code=status.HTTP_204_NO_CONTENT)
async def clear_driver():
    global drivers
    if len(drivers) > 0:
        for driver in drivers:
            driver.quit()
            rmtree(driver.capabilities['chrome']['userDataDir'])
        drivers.clear()
    else:
        raise HTTPException(status_code=404, detail="No driver to clear")