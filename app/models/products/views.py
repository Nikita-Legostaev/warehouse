from fastapi import APIRouter, Depends, HTTPException

from app.models.products.repositories import ProductsRepositories

router = APIRouter(
    prefix="/products",
    tags=["product"],
)


@router.get("/all")
async def get_all_products(offset: int = 0, limit: int = 10):
    all_products = await ProductsRepositories.get_all()
    return all_products[offset:limit]