from logging import Logger

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from dependencies import logger, stored_drivers
from services.driver import StoredDrivers

scraping_router = APIRouter()


@scraping_router.get("/scraping")
def scraping_home() -> HTMLResponse:
    return HTMLResponse(content="<h1>Scraping Home</h1>", status_code=200)


@scraping_router.get("/scraping/sections")
def scraping_sections(
    drivers: StoredDrivers = Depends(stored_drivers), logger: Logger = Depends(logger)
) -> None:
    pass
