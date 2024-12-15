from fastapi import FastAPI
from app.models.manufacturers.views import router as router_manufacturer
from app.models.product_categories.views import router as router_category
from app.models.products.views import router as router_product
from app.models.product_features.views import router as router_feature
from app.models.shipments.views import router as router_shipment
from app.models.stock.views import router as router_stock

from app.pages.router import router as router_pages

app = FastAPI()
app.include_router(router_manufacturer)
app.include_router(router_category)
app.include_router(router_product)
app.include_router(router_pages)
app.include_router(router_feature)
app.include_router(router_shipment)
app.include_router(router_stock)