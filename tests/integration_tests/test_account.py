

from os import access
from typing import List

import pytest
from domain.entities.account import Account, AccountCreate
from domain.exceptions.account import DuplicatedCPFException, DuplicatedEmailException, InvalidCarPlateException, InvalidCpfException
from domain.repositories import account
from domain.repositories.account import AccountRepository
from uuid import uuid4

from usecases.create_account import CreateAccount
from usecases.all_accounts import AllAccounts

DUPLICATED_CPF = "48011532081"
VALID_CPF = "57685832038"
INVALID_CPF_LIST = ["", "11111111111", "1nv4lid"]
VALID_EMAIL = "janedoe@gmail.com"
DUPLICATED_EMAIL = "johndoe@gmail.com"
VALID_PLATE = "abc1234"
INVALID_PLATE_LIST = ["", "1nv4l1d_pl4t3", "1", "aaa"]


class InMemoryAccountsRepository(AccountRepository):
    def __init__(self) -> None:
        self.accounts = [Account(id=str(uuid4()),
                                 name="johndoe",
                                 cpf="15202336047",
                                 email="johndoe@gmail.com",
                                 car_plate="aaa1234",
                                 is_passenger=False,
                                 is_driver=True),
                         Account(id=str(uuid4()),
                                 name="mariedoe",
                                 cpf="48011532081",
                                 email="mariedoe@gmail.com",
                                 car_plate=None,
                                 is_passenger=True,
                                 is_driver=False)]

    def all(self) -> List[Account]:
        return self.accounts

    def create(self, account: AccountCreate) -> None:
        created_account = Account(id=str(uuid4()),
                                  name=account.name,
                                  email=account.email,
                                  cpf=account.cpf,
                                  car_plate=account.car_plate,
                                  is_driver=account.is_driver,
                                  is_passenger=account.is_passenger)
        self.accounts.append(created_account)

    def delete_by_email(self, email: str) -> None:
        self.accounts = [account for account in self.accounts if account.email != email]


@pytest.fixture
def in_memory_accounts_repository() -> InMemoryAccountsRepository:
    return InMemoryAccountsRepository()


def test_should_retrieve_all_accouts(in_memory_accounts_repository: InMemoryAccountsRepository) -> None:
    all_accounts = AllAccounts(in_memory_accounts_repository)
    output = all_accounts.execute()
    assert len(output) != 0


def test_should_create_account(in_memory_accounts_repository: InMemoryAccountsRepository) -> None:

    account_create = AccountCreate(name="mariedoe",
                                   cpf=VALID_CPF,
                                   email=VALID_EMAIL,
                                   car_plate=None,
                                   is_passenger=True,
                                   is_driver=False)
    create_account = CreateAccount(in_memory_accounts_repository)
    create_account.execute(account_create)

    accounts = in_memory_accounts_repository.all()
    assert any(account for account in accounts if account.cpf == account_create.cpf) == True


def test_should_raise_duplicate_cpf_when_creating_account(in_memory_accounts_repository: InMemoryAccountsRepository) -> None:
    account_create = AccountCreate(name="mariedoe",
                                   cpf=DUPLICATED_CPF,
                                   email="mariedoe@gmail.com",
                                   car_plate=None,
                                   is_passenger=True,
                                   is_driver=False)

    create_account = CreateAccount(in_memory_accounts_repository)
    with pytest.raises(DuplicatedCPFException):
        create_account.execute(account_create)


def test_should_raise_duplicate_email_when_creating_account(in_memory_accounts_repository: InMemoryAccountsRepository) -> None:
    account_create = AccountCreate(name="mariedoe",
                                   cpf=VALID_CPF,
                                   email=DUPLICATED_EMAIL,
                                   car_plate=None,
                                   is_passenger=True,
                                   is_driver=False)

    create_account = CreateAccount(in_memory_accounts_repository)
    with pytest.raises(DuplicatedEmailException):
        create_account.execute(account_create)


@pytest.mark.parametrize("cpf", INVALID_CPF_LIST)
def test_should_raise_invalid_cpf_when_creating_account(cpf: str, in_memory_accounts_repository: InMemoryAccountsRepository) -> None:
    account_create = AccountCreate(name="mariedoe",
                                   cpf=cpf,
                                   email=VALID_EMAIL,
                                   car_plate=None,
                                   is_passenger=True,
                                   is_driver=False)

    create_account = CreateAccount(in_memory_accounts_repository)
    with pytest.raises(InvalidCpfException):
        create_account.execute(account_create)


@pytest.mark.parametrize("plate", INVALID_PLATE_LIST)
def test_when_driver_has_invalid_plate_raise_error(plate: str, in_memory_accounts_repository: InMemoryAccountsRepository) -> None:
    account_create = AccountCreate(name="mariedoe",
                                   cpf=VALID_CPF,
                                   email=VALID_EMAIL,
                                   car_plate=plate,
                                   is_passenger=False,
                                   is_driver=True)

    create_account = CreateAccount(in_memory_accounts_repository)
    with pytest.raises(InvalidCarPlateException):
        create_account.execute(account_create)


def test_create_passenger_when_assert_plate_is_not_created(in_memory_accounts_repository: InMemoryAccountsRepository) -> None:
    account_create = AccountCreate(name="mariedoe",
                                   cpf=VALID_CPF,
                                   email=VALID_EMAIL,
                                   car_plate=VALID_PLATE,
                                   is_passenger=True,
                                   is_driver=False)

    create_account = CreateAccount(in_memory_accounts_repository)
    create_account.execute(account_create)

    existing_account = next(account for account in in_memory_accounts_repository.all()
                            if account.cpf == account_create.cpf)

    assert existing_account.car_plate is None


def test_should_raise_when_create_driver_with_no_plate(in_memory_accounts_repository: InMemoryAccountsRepository) -> None:
    account_create = AccountCreate(name="mariedoe",
                                   cpf=VALID_CPF,
                                   email=VALID_EMAIL,
                                   car_plate=None,
                                   is_passenger=False,
                                   is_driver=True)
    create_account = CreateAccount(in_memory_accounts_repository)
    with pytest.raises(InvalidCarPlateException) as exc:
        create_account.execute(account_create)


def test_should_create_driver(in_memory_accounts_repository: InMemoryAccountsRepository) -> None:
    account_create = AccountCreate(name="mariedoe",
                                   cpf=VALID_CPF,
                                   email=VALID_EMAIL,
                                   car_plate=VALID_PLATE,
                                   is_passenger=False,
                                   is_driver=True)
    create_account = CreateAccount(in_memory_accounts_repository)
    create_account.execute(account_create)
