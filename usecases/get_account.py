
from typing import List
from domain.exceptions.account import AccountNotFoundException
from domain.repositories.account import AccountRepository
from domain.entities.account import Account


class GetAccount:
    def __init__(self, account_repository: AccountRepository) -> None:
        self.account_repository = account_repository

    def execute(self, email: str) -> Account:
        existing_account = self.account_repository.find(email)
        if not existing_account:
            raise AccountNotFoundException()
        
        return existing_account
