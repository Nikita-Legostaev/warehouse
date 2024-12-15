from fastapi import APIRouter, Depends, HTTPException

from app.models.shipments.repositories import ShipmentsRepositories
from app.models.shipments.shemas import SShipments

router = APIRouter(
    prefix="/shipments",
    tags=["shipment"],
)


@router.get("/all")
async def get_all_shipments(offset: int = 0, limit: int = 10):
    all_shipments = await ShipmentsRepositories.get_all()
    return all_shipments[offset:limit]


@router.post("/add")
async def add_shipments(
    SShipments: SShipments,
):
    await ShipmentsRepositories.add(
        product_id=SShipments.product_id,
        shipment_date=SShipments.shipment_date,
        quantity=SShipments.quantity,
        supplier_name=SShipments.supplier_name,
    )
    return {"detail": "Успешно"}


@router.delete("/remove/{shipments_id}")
async def remove_shipments(
    shipments_id: int,
):
    shipments = await ShipmentsRepositories.find_one_or_none(id=shipments_id)
    if not shipments:
        raise HTTPException(status_code=404, detail="Не найдено")
    await ShipmentsRepositories.delete(id=shipments_id)
    return {"detail": "Успешно удалено"}


@router.patch("/edit/{shipments_id}")
async def update_shipments(
    shipments_id: int,
    SShipments: SShipments,  
    ):
    shipments = await ShipmentsRepositories.find_by_id(id=shipments_id)
    if not shipments:
        raise HTTPException(status_code=404, detail="Не найдено")
    await ShipmentsRepositories.update(id=shipments_id, **SShipments.model_dump())
    return {"detail": "Успешно изменено"}

@router.get("/count")
async def count_stock():
    count = await ShipmentsRepositories.count()
    return {"count": count}