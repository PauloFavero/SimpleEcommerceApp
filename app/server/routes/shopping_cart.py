from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Path, HTTPException
from pymongo.errors import DuplicateKeyError

from entities import ShoppingCart, CartItem
from infra import ShoppingCartModel
from infra.mongo.repository import ShoppingCartRepository

shopping_cart_router = APIRouter(
    prefix="/shopping-cart",
    tags=["Shopping Cart API"],
)

shopping_cart_repo = ShoppingCartRepository()


@shopping_cart_router.get(
    "/{id}",
    status_code=HTTPStatus.OK,
)
async def get_shopping_cart(id: str = Path(..., regex=r"^[0-9a-f]{24}$")) -> ShoppingCartModel:
    shopping_cart = shopping_cart_repo.get_shopping_cart_by_id(id)
    print('get_shopping_cart', shopping_cart)
    if not shopping_cart:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Shopping Cart not found",
        )
    return shopping_cart


@shopping_cart_router.post("/", status_code=HTTPStatus.CREATED)
def create_shopping_cart(shopping_cart: ShoppingCart) -> str:
    try:
        shopping_cart_id = shopping_cart_repo.create_shopping_cart(shopping_cart)
        shopping_cart_repo.create_shopping_cart(shopping_cart_id)
        return shopping_cart_id
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
    
@shopping_cart_router.post("/{id}/add-items", status_code=HTTPStatus.CREATED)
def add_items_to_cart(items: List[CartItem], id: str = Path(..., regex=r"^[0-9a-f]{24}$")) -> str:
    result = shopping_cart_repo.add_items(id, items)
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Shopping Cart not found",
        )
    
    return "Items added to cart."

@shopping_cart_router.post("/{id}/remove-items", status_code=HTTPStatus.CREATED)
def remove_items_to_cart(items: List[str], id: str = Path(..., regex=r"^[0-9a-f]{24}$")) -> str:
    result = shopping_cart_repo.remove_items(id, items)
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Shopping Cart not found",
        )
    
    return f"Items {items} removed from cart."


@shopping_cart_router.put("/{id}", status_code=HTTPStatus.OK)
def clear_shopping_cart(id: str = Path(..., regex=r"^[0-9a-f]{24}$")) -> None:
    success = shopping_cart_repo.clear_cart(id)
    if not success:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="ShoppingCart not found",
        )
    return f"Shopping Cart for user {id} cleared."


@shopping_cart_router.delete("/{id}", status_code=HTTPStatus.OK)
def delete_shopping_cart(id: str = Path(..., regex=r"^[0-9a-f]{24}$")) -> None:
    success = shopping_cart_repo.delete_shopping_cart(id)
    if not success:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="ShoppingCart not found",
        )
    return f"Shopping Cart {id} deleted."
