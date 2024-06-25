import os
import shutil
from pathlib import Path
from time import time

import pytest
from dotenv import load_dotenv

from src.services.driver import (
    StoredDrivers,
    generate_driver_instances,
    webdriver_profile_generator,
)
from src.services.scraping.permission_passing import Credentials

load_dotenv(".env")


def random_path(base_dir: Path | str) -> Path:
    if isinstance(base_dir, str):
        return Path(base_dir) / hash(time()).__str__()
    elif isinstance(base_dir, Path):
        return base_dir / hash(time()).__str__()


def get_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Environment variable {key} is not set.")
    else:
        return value


LOGIN_URL = get_env("LOGIN_URL")
SECTION_TEST_URL = get_env("SECTION_TEST_URL")
COURSES_TEST_URL = get_env("COURSES_TEST_URL")
FILES_TEST_URL = get_env("FILES_TEST_URL")


@pytest.fixture
def cred() -> Credentials:
    load_dotenv(".env")

    # 環境変数からログイン情報を取得
    return Credentials(
        email=get_env("COLLAGE_EMAIL"),
        name=get_env("COLLAGE_USERNAME"),
        password=get_env("COLLAGE_PASSWORD"),
    )


@pytest.fixture
def test_driver(cred: Credentials):
    test_dir = random_path("tests/__pycache__/chrome_driver")
    test_dir.mkdir(parents=True, exist_ok=True)

    driver_generator = generate_driver_instances(
        profile_gen=webdriver_profile_generator(test_dir),
        driver_arguments=["--headless=new"],
        cred=cred,
    )

    driver = next(driver_generator)
    yield driver

    driver.quit()
    if test_dir.exists():
        shutil.rmtree(test_dir)


@pytest.fixture(scope="module")
def stored_drivers_and_dir():
    test_dir = random_path("tests/__pycache__/chrome_driver")
    test_dir.mkdir(parents=True, exist_ok=True)

    email = get_env("COLLAGE_EMAIL") or ""
    username = get_env("COLLAGE_USERNAME") or ""
    password = get_env("COLLAGE_PASSWORD") or ""

    if not email or not username or not password:
        pytest.skip("環境変数が設定されていないため、テストをスキップします")

    drivers: StoredDrivers | None = None
    try:
        drivers = StoredDrivers(
            profile_dir=test_dir,
            driver_args=["--headless=new"],
            cred=Credentials(email, username, password),
        )

        yield (drivers, test_dir)
    finally:
        drivers.clear()  # type: ignore
        if test_dir.exists():
            shutil.rmtree(test_dir)
