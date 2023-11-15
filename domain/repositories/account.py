from typing import List, Optional
from abc import ABC, abstractmethod
from domain.entities.account import Account, AccountCreate


class AccountRepository(ABC):
    @abstractmethod
    def all(self) -> List[Account]:
        pass
    
    @abstractmethod
    def create(self, account: AccountCreate) -> None:
        pass
