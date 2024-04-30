import pytest
from fastapi.testclient import TestClient
from typing import Generator, Any
from src import main

# classroomの構成は以下の通り
# section -> course -> file
# windowsにて、hypervisorがoffになっている場合、lifespanの部分でこけるため注意
# sleniumのインスタンス生成はこれをautoにしないとダメみたいだ

@pytest.fixture(scope="module")
def client() -> Generator[TestClient, Any, None]:
    with TestClient(main.app) as client:
        yield client

def test_route(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_get_sections(client: TestClient):
    response = client.get("/sections")
    assert response.status_code == 200
    assert response.json() == {}