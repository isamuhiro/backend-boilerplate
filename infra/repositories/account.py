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
        account_model = AccountModel(account_id=uuid.uuid4(),
                                     name=account.name,
                                     email=account.email,
                                     cpf=account.cpf,
                                     car_plate=account.car_plate,
                                     is_driver=account.is_driver,
                                     is_passenger=account.is_passenger)
        session.add(account_model)
        session.commit()
