import os
from shutil import rmtree
from fastapi import APIRouter, HTTPException, status, Depends

import dependencies as dep
from services.driver import *

driver_router = APIRouter()

@driver_router.get("/list")
async def list(logger = Depends(dep.logger), drivers = Depends(dep.stored_drivers)):
    return [str(driver) for driver in drivers]