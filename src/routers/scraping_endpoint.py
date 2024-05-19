from logging import Logger
from threading import Thread, Lock

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from selenium.webdriver.remote.webdriver import WebDriver

from dependencies import stored_drivers, logger
from services.driver import StoredDrivers
from services.scraping.page_objects import sections, courses, files, WhereIsDriver, DriverState, Credentials

scraping_router = APIRouter()

@scraping_router.get("/scraping")
def scraping_home():
    return HTMLResponse(content="<h1>Scraping Home</h1>", status_code=200)

@scraping_router.get("/scraping/sections")
def scraping_sections(drivers: StoredDrivers = Depends(stored_drivers), logger: Logger = Depends(logger)):
    driver: WebDriver = drivers[0]
    
    WhereIsDriver.of(driver.current_url) is DriverState.Pre