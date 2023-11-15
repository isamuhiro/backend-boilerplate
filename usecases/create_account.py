from domain.entities.cpf import clean_cpf, validate_cpf
from domain.entities.plate import clean_plate, validate_plate
from domain.exceptions.account import DuplicatedEmailException, InvalidCarPlateException, InvalidCpfException
from domain.repositories.account import AccountRepository
from domain.entities.account import AccountCreate


class CreateAccount:
    def __init__(self, account_repository: AccountRepository) -> None:
        self.account_repository = account_repository

    def execute(self, account_create: AccountCreate) -> None:
        is_cpf_invalid = not validate_cpf(account_create.cpf)

        if is_cpf_invalid:
            raise InvalidCpfException

        account_create.cpf = clean_cpf(account_create.cpf)

        accounts = self.account_repository.all()

        email_exists = any(
            account for account in accounts if account.email == account_create.email)

        if email_exists:
            raise DuplicatedEmailException

        if account_create.is_driver and account_create.car_plate:
            if not validate_plate(account_create.car_plate):
                raise InvalidCarPlateException()

            account_create.car_plate = clean_plate(account_create.car_plate)

        return self.account_repository.create(account=account_create)
