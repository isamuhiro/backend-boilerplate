from typing import List, Optional
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
                                     is_passenger=account.is_passenger,
                                     password=account.password)
        session.add(account_model)
        session.commit()

    def delete_by_email(self, email: str) -> None:
        existing_account = session.query(AccountModel).filter_by(email=email).first()
        if not existing_account:
            raise Exception("Account not found")
        
        session.delete(existing_account)
        session.commit()
        
    def delete(self) -> None:
        return None
    
    def find(self, email: str) -> Optional[Account]:
       existing_account = session.query(AccountModel).filter_by(email=email).first()
       if not existing_account:
           return None
       
       return existing_account.to_account()
   
    def find_by_id(self, id: str) -> Optional[Account]:
       existing_account = session.query(AccountModel).filter_by(uuid=id).first()
       if not existing_account:
           return None
       
       return existing_account.to_account()
    
        
