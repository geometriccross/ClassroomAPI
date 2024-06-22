from contextlib import asynccontextmanager
from os import getenv
from pathlib import Path

from fastapi import FastAPI

import dependencies as dep
from routers.scraping_endpoint import scraping_router
from services.driver import StoredDrivers


@asynccontextmanager
async def lifespan(app: FastAPI):
    appdata_path = getenv("APPDATA") or ""  # Provide a default value if "APPDATA" is None
    __stored_drivers = StoredDrivers(
        profile_dir=Path(appdata_path).joinpath("classroomAPI/chromedrivers"),
        driver_args=["--headless=new"],
    )

    dep.__stored_drivers = __stored_drivers

    try:
        yield
    finally:
        __stored_drivers.clear()


app = FastAPI(lifespan=lifespan)
app.include_router(scraping_router)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
