from logging import Logger, getLogger

from services.driver import StoredDrivers

__stored_drivers: StoredDrivers | None = None


def stored_drivers() -> StoredDrivers:
    if __stored_drivers is None:
        raise ValueError("StoredDrivers is not initialized")
    else:
        return __stored_drivers


def logger() -> Logger:
    return getLogger(__name__)
