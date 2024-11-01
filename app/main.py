from fastapi import FastAPI
from app.models.manufacturers.views import router as router_manufacturer
from app.models.product_categories.views import router as router_category
from app.models.products.views import router as router_product

app = FastAPI()
app.include_router(router_manufacturer)
app.include_router(router_category)
app.include_router(router_product)
