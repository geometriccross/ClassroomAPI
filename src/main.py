from os import getenv
from pathlib import Path
from fastapi import FastAPI
from contextlib import asynccontextmanager
from logging import Logger, getLogger

import dependencies as dep
from services.driver import StoredDrivers
from routers.scraping_endpoint import scraping_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    __stored_drivers = StoredDrivers(
        profile_dir = Path(getenv("APPDATA")).joinpath("classroomAPI/chromedrivers"),
        driver_arguments = ["--headless=new"]
    )
    
    dep.__stored_drivers = __stored_drivers

    try:
        yield
    finally:
        __stored_drivers.clear()

app = FastAPI(lifespan=lifespan)
app.include_router(scraping_router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)