from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.models.manufacturers.views import get_all_manufacturers
from app.models.product_categories.views import get_all_categories
from app.models.products.views import get_all_products


router = APIRouter(prefix='/pages', tags=['Фронтенд'])
templates = Jinja2Templates(directory='app/templates')


@router.get('/manufacturers')
async def get_manufacturers_html(request: Request, manufacturers=Depends(get_all_manufacturers)):
    return templates.TemplateResponse(name='manufacturers.html', context={'request': request, 'manufacturers': manufacturers})

@router.get('/categories')
async def get_categories_html(request: Request, categories=Depends(get_all_categories)):
    return templates.TemplateResponse(name='categories.html', context={'request': request, 'categories': categories})

@router.get('/products')
async def get_products_html(request: Request, products=Depends(get_all_products)):
    return templates.TemplateResponse(name='products.html', context={'request': request, 'products': products})