from fastapi import APIRouter, HTTPException, status
from services.scraping import *

scraping_router = APIRouter()

@scraping_router.get("/sections")
async def get_sections():
    global drivers
    data = {}
    try:
        data.update(sections(drivers[0], 10))
        return data
    except TimeoutError:
        raise HTTPException(status_code=500, detail="TimeoutError")