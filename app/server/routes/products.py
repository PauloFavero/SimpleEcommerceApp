from http import HTTPStatus

from fastapi import APIRouter, Path, HTTPException
from pymongo.errors import DuplicateKeyError

from entities import Product, UpdateProduct
from infra import ProductModel, PaginatedProductsModel
from infra.mongo.repository import ProductsRepository

products_router = APIRouter(
    prefix="/products",
    tags=["Products API"],
)

products_repo = ProductsRepository()


@products_router.get("/", status_code=HTTPStatus.OK)
async def get_products(
    page: int = 1,
    limit: int = 10,
    sort_order: int = 1,
    sort_by: str = "name",
    category_filter: str = None,
) -> PaginatedProductsModel:
    products = products_repo.get_all_products(
        page=page,
        limit=limit,
        sort_order=sort_order,
        sort_by=sort_by,
        category_filter=category_filter,
    )
    if len(products.data) == 0:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Products not found",
        )
    return products


@products_router.get(
    "/{id}",
    status_code=HTTPStatus.OK,
)
async def get_product(id: str = Path(..., regex=r"^[0-9a-f]{24}$")) -> ProductModel:
    product = products_repo.get_product_by_id(id)
    if not product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Product not found",
        )
    return product


# create new product
@products_router.post("/", status_code=HTTPStatus.CREATED)
def add_product(product: Product) -> str:
    try:
        return products_repo.create_product(product)
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


# partially update product
@products_router.patch("/{id}", status_code=HTTPStatus.OK)
def update_product(
    product: UpdateProduct, id: str = Path(..., regex=r"^[0-9a-f]{24}$")
) -> None:
    success = products_repo.update_product(id, product)
    if not success:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Product not found",
        )
    return f"Product {id} updated"


@products_router.put("/{id}", status_code=HTTPStatus.OK)
def replace_product_data(
    product: Product, id: str = Path(..., regex=r"^[0-9a-f]{24}$")
) -> None:
    success = products_repo.replace_product_data(id, product)
    if not success:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Product not found",
        )
    return f"Product {id} data replaced"
 

@products_router.delete("/{id}", status_code=HTTPStatus.OK)
def delete_product(id: str = Path(..., regex=r"^[0-9a-f]{24}$")) -> None:
    success = products_repo.delete_product(id)
    if not success:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Product not found",
        )
    return f"Product {id} deleted"
