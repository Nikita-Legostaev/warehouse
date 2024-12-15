from fastapi import APIRouter, Depends, HTTPException

from app.models.stock.repositories import StockRepositories
from app.models.stock.shemas import SStock

router = APIRouter(
    prefix="/stocks",
    tags=["stock"],
)


@router.get("/all")
async def get_all_stock(offset: int = 0, limit: int = 10):
    all_stock = await StockRepositories.get_all()
    return all_stock[offset:limit]


@router.post("/add")
async def add_stock(
    SStock: SStock,
):
    await StockRepositories.add(
        row=SStock.row,
        cell=SStock.cell,   
    )
    return {"detail": "Успешно"}


@router.delete("/remove/{stock_id}")
async def remove_stock(
    stock_id: int,
):
    stock = await StockRepositories.find_one_or_none(id=stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Не найдено")
    await StockRepositories.delete(id=stock_id)
    return {"detail": "Успешно удалено"}


@router.patch("/edit/{stock_id}")
async def update_stock(
    stock_id: int,
    SStock: SStock,  
    ):
    stock = await StockRepositories.find_by_id(id=stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Не найдено")
    await StockRepositories.update(id=stock_id, **SStock.model_dump())
    return {"detail": "Успешно изменено"}

@router.get("/count")
async def count_stock():
    count = await StockRepositories.count()
    return {"count": count}