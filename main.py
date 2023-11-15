from http import HTTPStatus
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from domain.exceptions.account import (DuplicatedCPFException, DuplicatedEmailException,
                                       InvalidCarPlateException,
                                       InvalidCpfException,
                                       InvalidEmailException)

from domain.entities.account import Account, AccountCreate
from infra.repositories.account import DatabaseAccountRepository
from usecases.all_accounts import AllAccounts
from usecases.create_account import CreateAccount

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


@app.post("/accounts")
async def create_account(account_create: AccountCreate) -> None:
    try:
        create_account = CreateAccount(DatabaseAccountRepository())
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
