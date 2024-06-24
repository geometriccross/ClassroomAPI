import shutil
from os import getenv, makedirs, path
from pathlib import Path

import pytest
from dotenv import load_dotenv

from src.services import driver
from src.services.scraping.permission_passing import Credentials

TEST_DIR = Path("tests/chrome_drivers")

load_dotenv(".env")


@pytest.fixture(scope="module")
def drivers():
    if path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)

    email = getenv("COLLAGE_EMAIL") or ""
    username = getenv("COLLAGE_USERNAME") or ""
    password = getenv("COLLAGE_PASSWORD") or ""

    if not email or not username or not password:
        pytest.skip("環境変数が設定されていないため、テストをスキップします")

    drivers: driver.StoredDrivers | None = None
    try:
        makedirs(TEST_DIR, exist_ok=True)
        drivers = driver.StoredDrivers(
            profile_dir=TEST_DIR,
            driver_args=["--headless=new"],
            cred=Credentials(email, username, password),
        )

        yield drivers
    finally:
        drivers.clear()  # type: ignore
        if path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)


def test_webdriver_profile_generator():
    profile_generator = driver.webdriver_profile_generator(Path(""))
    assert next(profile_generator) == Path("profile_0")
    assert next(profile_generator) == Path("profile_1")

    profile_generator = driver.webdriver_profile_generator(Path(""), 5)
    assert next(profile_generator) == Path("profile_5")


def test_stored_drivers_shrink(drivers: driver.StoredDrivers):
    drivers.shrink()
    assert len(drivers) == 0, "正常にshrinkできているか確認"

    # 異常を起こさないか確認
    drivers.shrink()

    ins_index = 3
    for _ in range(ins_index):
        drivers.grow()

    assert len(drivers) == ins_index
    drivers.shrink()
    ins_index -= 1

    assert TEST_DIR.joinpath(f"profile_{ins_index-1}").exists()
    drivers.grow()
    ins_index += 1

    assert TEST_DIR.joinpath(
        f"profile_{ins_index-1}"
    ).exists(), "削除後に再びgrowした場合、indexの位置が正しく継続されているかどうか"
