import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, status
from selenium.webdriver.remote.webdriver import WebDriver

from contextlib import asynccontextmanager

from src.routers.driver import driver_router
from src.routers.scraping import scraping_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    global drivers
    global instance_gen
    # アプリケーションの起動時にドライバーを作成
    drivers.append(next(instance_gen))

    yield

    for driver in drivers:
        driver.quit()

app = FastAPI(lifespan=lifespan)
app.include_router(driver_router)
app.include_router(scraping_router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}