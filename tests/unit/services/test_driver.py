from pathlib import Path

from src.services import driver


def test_webdriver_profile_generator():
    profile_generator = driver.webdriver_profile_generator(Path(""))
    assert next(profile_generator) == Path("profile_0")
    assert next(profile_generator) == Path("profile_1")

    profile_generator = driver.webdriver_profile_generator(Path(""), 5)
    assert next(profile_generator) == Path("profile_5")


def test_stored_drivers_shrink(stored_drivers_and_dir: tuple[driver.StoredDrivers, Path]):
    stored_drivers = stored_drivers_and_dir[0]
    test_dir = stored_drivers_and_dir[1]

    stored_drivers.shrink()
    assert len(stored_drivers) == 0, "正常にshrinkできているか確認"

    # 異常を起こさないか確認
    stored_drivers.shrink()

    ins_index = 3
    for _ in range(ins_index):
        stored_drivers.grow()

    assert len(stored_drivers) == ins_index
    stored_drivers.shrink()
    ins_index -= 1

    assert test_dir.joinpath(f"profile_{ins_index-1}").exists()
    stored_drivers.grow()
    ins_index += 1

    "削除後に再びgrowした場合、indexの位置が正しく継続されているかどうか"
    assert test_dir.joinpath(f"profile_{ins_index-1}").exists()
