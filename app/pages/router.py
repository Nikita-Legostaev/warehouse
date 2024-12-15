from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.models.manufacturers.views import get_all_manufacturers, count_stock
from app.models.product_categories.views import get_all_categories, count_stock
from app.models.products.views import get_all_products, count_stock
from app.models.product_features.views import get_all_product_features, count_stock
from app.models.shipments.views import get_all_shipments, count_stock
from app.models.stock.views import get_all_stock, count_stock

from app.models.manufacturers.repositories import ManufacturersRepositories
from app.models.product_categories.repositories import CategoryRepositories
from app.models.products.repositories import ProductsRepositories
from app.models.product_features.repositories import Product_featuresRepositories
from app.models.shipments.repositories import ShipmentsRepositories
from app.models.stock.repositories import StockRepositories



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

@router.get('/product_features')
async def get_product_features_html(request: Request, product_features=Depends(get_all_product_features)):
    return templates.TemplateResponse(name='product_features.html', context={'request': request, 'product_features': product_features})

@router.get('/shipments')
async def get_shipments_html(request: Request, shipments=Depends(get_all_shipments)):
    return templates.TemplateResponse(name='shipments.html', context={'request': request, 'shipments': shipments})

@router.get('/stock')
async def get_stock_html(request: Request, stock=Depends(get_all_stock)):
    return templates.TemplateResponse(name='stock.html', context={'request': request, 'stock': stock})

@router.get('/count')
async def get_counts_html(
    request: Request,
    count_manufactures=Depends(ManufacturersRepositories.count),  # Подсчет производителей
    count_categories=Depends(CategoryRepositories.count),        # Подсчет категорий
    count_products=Depends(ProductsRepositories.count),             # Подсчет продуктов
    count_product_features=Depends(Product_featuresRepositories.count), # Подсчет характеристик продуктов
    count_shipments=Depends(ShipmentsRepositories.count),           # Подсчет поставок
    count_stock=Depends(StockRepositories.count)                    # Подсчет запасов
):
    # Подготовка данных для диаграммы
    counts_data = {
        'Manufacturers': count_manufactures,
        'Categories': count_categories,
        'Products': count_products,
        'Product Features': count_product_features,
        'Shipments': count_shipments,
        'Stock': count_stock
    }

    return templates.TemplateResponse(
        'counts.html', 
        context={'request': request, 'counts_data': counts_data}
    )