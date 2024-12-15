from fastapi import APIRouter, Depends, HTTPException
from pydantic import TypeAdapter

from app.models.manufacturers.repositories import ManufacturersRepositories
from app.models.manufacturers.shemas import SManufact


router = APIRouter(
    prefix="/manufacturers",
    tags=["manufacturers"],
)


@router.get("/all")
async def get_all_manufacturers(offset: int = 0, limit: int = 10):
    all_manufacturers = await ManufacturersRepositories.get_all()
    return all_manufacturers[offset:limit]

@router.post("/add")
async def add_manufactor(
    SManufacturers: SManufact,
):
    await ManufacturersRepositories.add(
        manufacturer_name=SManufacturers.manufacturer_name,
        address=SManufacturers.address,
        email=SManufacturers.email,
    )
    return {"detail": "Успешно"}


@router.delete("/remove/{manufactors_id}")
async def remove_manufactors(
    manufactors_id: int,
):
    manufactor = await ManufacturersRepositories.find_one_or_none(id=manufactors_id)
    if not manufactor:
        raise HTTPException(status_code=404, detail="Не найдено")
    await ManufacturersRepositories.delete(id=manufactors_id)
    return {"detail": "Успешно удалено"}


@router.patch("/edit/{manufactors_id}")
async def update_manufactors(
    manufactors_id: int,
    SManufacturers: SManufact,  
    ):
    manufactor = await ManufacturersRepositories.find_by_id(id=manufactors_id)
    if not manufactor:
        raise HTTPException(status_code=404, detail="Не найдено")
    await ManufacturersRepositories.update(id=manufactors_id, **SManufacturers.model_dump())
    return {"detail": "Успешно изменено"}


@router.get("/count")
async def count_stock():
    count = await ManufacturersRepositories.count()
    return {"count": count}