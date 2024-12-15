from fastapi import APIRouter, Depends, HTTPException

from app.models.products.repositories import ProductsRepositories
from app.models.products.shemas import SPorducts
from datetime import date

router = APIRouter(
    prefix="/products",
    tags=["product"],
)


@router.get("/all")
async def get_all_products(offset: int = 0, limit: int = 10):
    all_products = await ProductsRepositories.get_all()
    return all_products[offset:limit]


@router.post("/add")
async def add_products(
    SPorducts: SPorducts,
):
    await ProductsRepositories.add(
        product_name=SPorducts.product_name,
        manufacturer_id=SPorducts.manufacturer_id,
        category_id=SPorducts.category_id,
        price=SPorducts.price,
        expiration_date=SPorducts.expiration_date,
        weight=SPorducts.weight,
        stock_id=SPorducts.stock_id,
        stock_location=SPorducts.stock_location,
        stock_quantity=SPorducts.stock_quantity, 
    )
    return {"detail": "Успешно"}


@router.delete("/remove/{products_id}")
async def remove_products(
    products_id: int,
):
    products = await ProductsRepositories.find_one_or_none(id=products_id)
    if not products:
        raise HTTPException(status_code=404, detail="Не найдено")
    await ProductsRepositories.delete(id=products_id)
    return {"detail": "Успешно удалено"}


@router.patch("/edit/{products_id}")
async def update_products(
    products_id: int,
    SPorducts: SPorducts,  
    ):
    products = await ProductsRepositories.find_by_id(id=products_id)
    if not products:
        raise HTTPException(status_code=404, detail="Не найдено")
    await ProductsRepositories.update(id=products_id, **SPorducts.model_dump())
    return {"detail": "Успешно изменено"}

@router.get("/search/")
async def search_products(
    offset: int = 0, limit: int = 10,
    product_name: str = None,
    manufacturer_id: int = None,
    category_id: int = None,
    price: int = None,
    expiration_date: date = None,
    weight: int = None,
    stock_id: int = None,
    stock_location: int = None,
    stock_quantity: int  = None,
):
    filter_params = {key: value for key, value in locals().items() if value is not None and key not in ['offset', 'limit']}
    
    products = await ProductsRepositories.get_all(**filter_params)
    
    if not products:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    
    return products[offset:offset + limit]

@router.get("/count")
async def count_stock():
    count = await ProductsRepositories.count()
    return {"count": count}