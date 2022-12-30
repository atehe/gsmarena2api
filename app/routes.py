from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import joinedload

from gsmarena_scraper import GSMArenaScraper

from . import schemas
from .database import db_session
from .models import Brand, Device, DeviceSpecification
from .utils import paginate_model

router = APIRouter()


@router.get("/update_db", response_model=schemas.Response)
async def update_db():
    scraper = GSMArenaScraper()
    scraper.open_aws_gateway()
    scraper.parse_devices()
    scraper.close_aws_gateway()


@router.get("/brands", response_model=schemas.BrandsResponse)
async def get_brands(page: int = 1, limit: int = 10):
    total_brands = db_session.query(Brand).count()
    brands = paginate_model(db_session, Brand, page, limit)

    return dict(total_brands=total_brands, brands=brands, page=page, size=limit)


@router.get("/brands/{brand_id}", response_model=schemas.BrandDevicesResponse)
async def get_devices(brand_id: str, page: int = 1, limit: int = 10):
    brand = db_session.query(Brand).get(brand_id)
    if brand is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found"
        )

    devices = paginate_model(db_session, Device, page, limit, brand=brand)

    return dict(
        brand=brand,
        devices=devices,
        size=limit,
        page=page,
        total_devices=brand.num_devices
    )


@router.get("/devices/{device_id}", response_model=schemas.DeviceSpecDetail)
async def get_device_specificaitions(device_id: str):
    device = db_session.query(Device) \
        .options(joinedload(Device.specs), joinedload(Device.brand)) \
        .get(device_id)

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found"
        )

    grouped_specs = dict()
    for spec in device.specs:
        spec: DeviceSpecification
        category = spec.spec_category
        specification = spec.specification

        grouped_specs.setdefault(category, {})
        grouped_specs[category][specification] = spec.spec_value

    return dict(device=device, brand=device.brand, specifications=grouped_specs)


@router.get("/devices", response_model=schemas.DevicesResponse)
async def all_devices(page: int = 1, limit: int = 10):
    total_devices = db_session.query(Device).count()
    devices = paginate_model(db_session, Device, page, limit)

    return dict(devices=devices, total_devices=total_devices, page=page, size=limit)
