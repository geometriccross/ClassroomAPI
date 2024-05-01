import os
import pytest
from fastapi.testclient import TestClient
from typing import Generator, Any
from dotenv import load_dotenv
from src import main
from src.scraping import login_to_google_classroom

# classroomの構成は以下の通り
# section -> course -> file
# windowsにて、hypervisorがoffになっている場合、lifespanの部分でこけるため注意
# sleniumのインスタンス生成はこれをautoにしないとダメみたいだ

load_dotenv(".env")

# 環境変数からログイン情報を取得
USER_NAME = os.getenv("COLLAGE_USERNAME")
USER_EMAIL = os.getenv("COLLAGE_EMAIL")
PASSWORD = os.getenv("COLLAGE_PASSWORD")

@pytest.fixture(scope="module")
def client() -> Generator[TestClient, Any, None]:
    with TestClient(main.app) as client:
        yield client

def test_route(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_get_sections(client: TestClient):
    login_to_google_classroom(main.drivers[0], USER_EMAIL, USER_NAME, PASSWORD)
    response = client.get("/sections")
    assert response.status_code == 200
    assert response.json() == {}