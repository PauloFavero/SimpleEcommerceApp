from http import HTTPStatus

from fastapi import APIRouter, Path, HTTPException
from pymongo.errors import DuplicateKeyError

from entities import User, UpdateUser
from infra import UserModel, PaginatedUsersModel
from infra.mongo.repository import UsersRepository, ShoppingCartRepository

user_router = APIRouter(
    prefix="/users",
    tags=["Users API"],
)

user_repo = UsersRepository()
shopping_cart_repo = ShoppingCartRepository()


@user_router.get("/", status_code=HTTPStatus.OK)
async def get_users(page: int = 1, limit: int = 10) -> PaginatedUsersModel:
    users = user_repo.get_all_users(page=page, limit=limit)
    if len(users.data) == 0:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Users not found",
        )
    return users


@user_router.get(
    "/{id}",
    status_code=HTTPStatus.OK,
)
async def get_user(id: str = Path(..., regex=r"^[0-9a-f]{24}$")) -> UserModel:
    user = user_repo.get_user_by_id(id)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )
    return user


# create new user with an empty shopping cart
@user_router.post("/", status_code=HTTPStatus.CREATED)
def add_user(user: User) -> str:
    try:
        user_id = user_repo.create_user(user)
        shopping_cart_repo.create_shopping_cart(user_id)
        return user_id
    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# partially update user
@user_router.patch("/{id}", status_code=HTTPStatus.OK)
def update_user(user: UpdateUser, id: str = Path(..., regex=r"^[0-9a-f]{24}$")) -> None:
    success = user_repo.update_user(id, user)
    if not success:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )
    return f"User {id} updated"


@user_router.put("/{id}", status_code=HTTPStatus.OK)
def replace_user_data(user: User, id: str = Path(..., regex=r"^[0-9a-f]{24}$")) -> None:
    success = user_repo.replace_user_data(id, user)
    if not success:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )
    return f"User {id} data replaced"


@user_router.delete("/{id}", status_code=HTTPStatus.OK)
def delete_user(id: str = Path(..., regex=r"^[0-9a-f]{24}$")) -> None:
    success = user_repo.delete_user(id)
    if not success:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )
    return f"User {id} deleted"
