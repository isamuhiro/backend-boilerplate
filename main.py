from http import HTTPStatus
from typing import Union, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from domain.exceptions.user import UserNotFoundException, InvalidUserCredentialsException, PasswordLengthException, \
    UsernameLengthException
from infra.models.user import UserLogin
from infra.repositories.user import InMemoryUserRepository
from usecases.authentication import AuthenticateUser

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
        authenticate_user = AuthenticateUser(user_repository=InMemoryUserRepository())
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
