from http import HTTPStatus
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from domain.exceptions.account import (AccountNotFoundException, DuplicatedCPFException, DuplicatedEmailException,
                                       InvalidCarPlateException,
                                       InvalidCpfException,
                                       InvalidEmailException, InvalidPasswordException)

from domain.entities.account import Account, AccountCreate
from infra.repositories.account import DatabaseAccountRepository
from usecases import get_account
from usecases.all_accounts import AllAccounts
from usecases.signup import Signup
from usecases.get_account import GetAccount

app = FastAPI()


class SmokeResponse(BaseModel):
    is_ok: bool


@app.get("/smoke")
async def root() -> dict[str, bool]:
    return {"is_ok": True}


@app.get("/accounts")
async def accounts() -> List[Account]:
    get_accounts = AllAccounts(DatabaseAccountRepository())
    return get_accounts.execute()


@app.get("/account/{email}")
async def find_account(email: str) -> Account:
    try:

        get_account = GetAccount(DatabaseAccountRepository())
        result = get_account.execute(email=email)
        return result
    except AccountNotFoundException:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Conta não encontrada")


@app.post("/accounts")
async def create_account(account_create: AccountCreate) -> None:
    try:
        create_account = Signup(DatabaseAccountRepository())
        create_account.execute(account_create)
    except InvalidCpfException:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="CPF inválido")
    except DuplicatedEmailException:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Email já cadastrado")
    except DuplicatedCPFException:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="CPF já cadastrado")
    except InvalidEmailException:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Email inválido")
    except InvalidCarPlateException:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Placa do carro inválida")
    except InvalidPasswordException:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Senha inválida")
