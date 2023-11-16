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

    @abstractmethod
    def delete_by_email(self, email: str) -> None:
        pass
    
    @abstractmethod
    def find(self, email: str) -> Optional[Account]:
        pass
    
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Account]:
        pass
