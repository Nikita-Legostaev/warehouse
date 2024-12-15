from fastapi import APIRouter, Depends, HTTPException

from app.models.product_categories.repositories import CategoryRepositories
from app.models.product_categories.shemas import SCategory


router = APIRouter(
    prefix="/products_categories",
    tags=["product_categories"],
)


@router.get("/all")
async def get_all_categories(offset: int = 0, limit: int = 10):
    all_category = await CategoryRepositories.get_all()
    return all_category[offset:limit]

@router.post("/add")
async def add_manufactor(
    SCategory: SCategory,
):
    await CategoryRepositories.add(
        category_name=SCategory.category_name
    )
    return {"detail": "Успешно"}


@router.delete("/remove/{category_id}")
async def remove_category(
    category_id: int,
):
    category = await CategoryRepositories.find_one_or_none(id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Не найдено")
    await CategoryRepositories.delete(id=category_id)
    return {"detail": "Успешно удалено"}


@router.patch("/edit/{category_id}")
async def update_category(
    category_id: int,
    SCategory: SCategory,  
    ):
    category = await CategoryRepositories.find_by_id(id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Не найдено")
    await CategoryRepositories.update(id=category_id, **SCategory.model_dump())
    return {"detail": "Успешно изменено"}


@router.get("/count")
async def count_stock():
    count = await CategoryRepositories.count()
    return {"count": count}