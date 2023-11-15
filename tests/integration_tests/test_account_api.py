from http import HTTPStatus
from typing import Any, Dict, Generator

import pytest
from fastapi.testclient import TestClient

from domain.entities.account import AccountCreate
from infra.repositories.account import DatabaseAccountRepository
from main import app

client = TestClient(app)


NEW_DRIVER = "newuser"
NEW_EMAIL_DRIVER = "newuser@gmail.com"
NEW_CPF_DRIVER = "31569037019"
NEW_PLATE = "zxy4321"

EXISTING_DRIVER = "johndoe"
EXISTING_CPF = "57685832038"
EXISTING_EMAIL = "johndoe@gmail.com"
EXISTING_PLATE = "abc1234"

INVALID_CPF_LIST = ["", "11111111111", "1nv4lid"]
INVALID_PLATE_LIST = ["", "1nv4l1d_pl4t3", "1", "aaa"]


@pytest.fixture
def new_driver() -> Generator[Any, Any, Any]:
    # BEFORE
    driver = {
        "name": NEW_DRIVER,
        "email": NEW_EMAIL_DRIVER,
        "cpf": NEW_CPF_DRIVER,
        "car_plate": NEW_PLATE,
        "is_driver": True,
        "is_passenger": False
    }

    yield driver

    # AFTER
    account_repository = DatabaseAccountRepository()
    account_repository.delete_by_email(email=str(driver["email"]))


def test_should_retrieve_200() -> None:
    response = client.get("/accounts")
    assert response.status_code == 200


def test_should_create_valid_driver(new_driver: Dict[Any, Any]) -> None:
    response = client.post("/accounts", json=new_driver)
    assert response.status_code == 200


def test_should_raise_duplicate_cpf_when_creating_account() -> None:
    account_create = AccountCreate(name=NEW_DRIVER,
                                   cpf=EXISTING_CPF,
                                   email=NEW_EMAIL_DRIVER,
                                   car_plate=NEW_PLATE,
                                   is_passenger=False,
                                   is_driver=True)

    response = client.post("/accounts", json=account_create.model_dump())
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_should_raise_duplicate_email_when_creating_account() -> None:
    account_create = AccountCreate(name=NEW_DRIVER,
                                   cpf=NEW_CPF_DRIVER,
                                   email=EXISTING_EMAIL,
                                   car_plate=None,
                                   is_passenger=False,
                                   is_driver=True)

    response = client.post("/accounts", json=account_create.model_dump())
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_should_raise_invalid_cpf_when_creating_account() -> None:
    account_create = AccountCreate(name=NEW_DRIVER,
                                   cpf=INVALID_CPF_LIST[0],
                                   email=NEW_EMAIL_DRIVER,
                                   car_plate=None,
                                   is_passenger=False,
                                   is_driver=True)

    response = client.post("/accounts", json=account_create.model_dump())
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_when_driver_has_invalid_plate_raise_error() -> None:
    account_create = AccountCreate(name=NEW_DRIVER,
                                   cpf=NEW_CPF_DRIVER,
                                   email=NEW_EMAIL_DRIVER,
                                   car_plate=INVALID_PLATE_LIST[0],
                                   is_passenger=False,
                                   is_driver=True)

    response = client.post("/accounts", json=account_create.model_dump())
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
