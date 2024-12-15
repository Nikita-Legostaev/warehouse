from fastapi import APIRouter, Depends, HTTPException

from app.models.product_features.repositories import Product_featuresRepositories
from app.models.product_features.shemas import SProductFeature


router = APIRouter(
    prefix="/product_features",
    tags=["product_features"],
)


@router.get("/all")
async def get_all_product_features(offset: int = 0, limit: int = 10):
    all_product_features = await Product_featuresRepositories.get_all()
    return all_product_features[offset:limit]

@router.post("/add")
async def add_product_features(
    SProductFeature: SProductFeature,
):
    await Product_featuresRepositories.add(
        feature_description=SProductFeature.feature_description
    )
    return {"detail": "Успешно"}


@router.delete("/remove/{product_features_id}")
async def remove_product_features(
    product_features_id: int,
):
    product_features = await Product_featuresRepositories.find_one_or_none(id=product_features_id)
    if not product_features:
        raise HTTPException(status_code=404, detail="Не найдено")
    await Product_featuresRepositories.delete(id=product_features_id)
    return {"detail": "Успешно удалено"}


@router.patch("/edit/{product_features_id}")
async def update_product_features(
    product_features_id: int,
    SProductFeature: SProductFeature,  
    ):
    product_features = await Product_featuresRepositories.find_by_id(id=product_features_id)
    if not product_features:
        raise HTTPException(status_code=404, detail="Не найдено")
    await Product_featuresRepositories.update(id=product_features_id, **SProductFeature.model_dump())
    return {"detail": "Успешно изменено"}

@router.get("/count")
async def count_stock():
    count = await Product_featuresRepositories.count()
    return {"count": count}