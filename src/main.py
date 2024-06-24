from contextlib import asynccontextmanager
from json import load
from os import getenv
from pathlib import Path

from fastapi import FastAPI

from routers.scraping_endpoint import scraping_router
from services.driver import Credentials, StoredDrivers


@asynccontextmanager
async def lifespan(app: FastAPI):
    app_path: Path = Path(path if (path := getenv("APPDATA")) is not None else ".")
    json_path = app_path.joinpath("config.json")

    if not json_path.exists():
        raise FileNotFoundError(f"{json_path} does not exist.")

    with json_path.open("r") as f:
        config: dict = load(f)

    cred: Credentials = config.get("credentials", None)
    if cred is None:
        raise ValueError("Credentials value not found in config.json.")

    stored_drivers = StoredDrivers(
        profile_dir=app_path.joinpath("classroomAPI/chromedrivers"),
        driver_args=["--headless=new"],
        cred=cred,
    )

    yield stored_drivers

    stored_drivers.clear()


app = FastAPI(lifespan=lifespan)  # type: ignore
app.include_router(scraping_router)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
