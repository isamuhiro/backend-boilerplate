from typing import List
import uuid
from domain.entities.account import Account, AccountCreate

from domain.repositories.account import AccountRepository
from infra.database.models.account import AccountModel
from infra.database.connection import session


class DatabaseAccountRepository(AccountRepository):
    def all(self) -> List[Account]:
        account_model_list = session.query(AccountModel).all()

        return [account.to_account() for account in account_model_list]

    def create(self, account: AccountCreate) -> None:
        account_model = AccountModel()
        account_model.account_id = uuid.uuid4()
        account_model.name = account.name
        account_model.email = account.email
        account_model.cpf = account.cpf
        account_model.car_plate = account.car_plate
        account_model.is_driver = account.is_driver
        account_model.is_passenger = account.is_passenger
        session.add(account_model)
        session.commit()
