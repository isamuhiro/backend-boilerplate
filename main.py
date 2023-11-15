from http import HTTPStatus
from typing import Union, Any, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from domain.exceptions.account import (DuplicatedEmailException,
                                       InvalidCarPlateException,
                                       InvalidCpfException,
                                       InvalidEmailException)

from domain.exceptions.user import (UserNotFoundException,
                                    InvalidUserCredentialsException,
                                    PasswordLengthException,
                                    UsernameLengthException)

from domain.entities.account import Account, AccountCreate
from infra.models.user import UserLogin
from infra.repositories.account import DatabaseAccountRepository
from infra.repositories.user import InMemoryUserRepository
from usecases.authentication import AuthenticateUser
from usecases.all_accounts import AllAccounts
from usecases.create_account import CreateAccount

app = FastAPI()


class SmokeResponse(BaseModel):
    is_ok: bool


@app.get("/smoke")
async def root() -> dict[str, bool]:
    return {"is_ok": True}


auth_responses: dict[Union[int, str], dict[str, Any]] = {
    HTTPStatus.OK.value: {"description": "User successfully logged in"},
    HTTPStatus.NOT_FOUND.value: {
        "description": "User Not Found",
        "content": {
            "application/json": {
                "example": {"detail": "User not found"}
            }
        }
    },
    HTTPStatus.UNAUTHORIZED.value: {
        "description": "Invalid User Credentials",
        "content": {
            "application/json": {
                "example": {"detail": "Invalid user credentials"}
            }
        }
    }
}


@app.post("/auth", responses=auth_responses)
async def auth(user_login: UserLogin) -> bool:
    try:
        authenticate_user = AuthenticateUser(
            user_repository=InMemoryUserRepository())
        authenticate_user.execute(user_login.to_user())
    except UserNotFoundException:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="User not found")
    except InvalidUserCredentialsException:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                            detail="Invalid user credentials")
    except PasswordLengthException:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            detail="Passwords must contain more than 9 characters")
    except UsernameLengthException:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                            detail="Username must contain more than 9 characters")
    return True


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
    except InvalidEmailException:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Email inválido")
    except InvalidCarPlateException:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Placa do carro inválida")
