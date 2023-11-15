
from typing import List
from domain.repositories.account import AccountRepository
from domain.entities.account import Account


class AllAccounts:
    def __init__(self, account_repository: AccountRepository) -> None:
        self.account_repository = account_repository

    def execute(self) -> List[Account]:
        return self.account_repository.all()
