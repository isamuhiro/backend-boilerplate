from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, UUID, Boolean
from domain.entities.account import Account
from typing import TYPE_CHECKING

Base = declarative_base()


class AccountModel(Base):  # type: ignore
    __tablename__ = 'account'
    __table_args__ = {'schema': 'cccat14'}


    account_id = Column(UUID, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    cpf = Column(String, nullable=False)
    email = Column(String, nullable=False)
    car_plate = Column(String, nullable=True)
    is_passenger = Column(Boolean, nullable=True)
    is_driver = Column(Boolean, nullable=True)

    def to_account(self) -> Account:
        account = Account(
            id=str(self.account_id),
            cpf=str(self.cpf),
            name=str(self.name),
            email=str(self.email),
            car_plate=str(self.car_plate),
            is_passenger=bool(self.is_passenger),
            is_driver=bool(self.is_driver))

        return account
