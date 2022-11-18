from fastapi import FastAPI
from model import db_session, Brand, Device, DeviceSpecification
from gsmarena_scraper import GSMArenaScraper


app = FastAPI()


@app.get("/update_db")
async def update_db():
    scraper = GSMArenaScraper()
    scraper.open_aws_gateway()
    scraper.parse_devices()
    scraper.close_aws_gateway()

    return {"success": True}


@app.get("/brands")
async def get_brands(page: int = 1, limit: int = 10):
    brands = db_session.query(Brand).all()

    formatted_brands = [brand.format() for brand in brands]

    start = (page - 1) * 10
    end = start + limit

    return {
        "success": True,
        "brands": formatted_brands[start:end],
        "total_brands": len(formatted_brands),
    }


@app.get("/brands/{brand_id}")
async def get_devices(brand_id, page: int = 1, limit: int = 10):
    devices = db_session.query(Device).filter_by(brand_id=brand_id)

    brand = db_session.query(Brand).filter_by(id=brand_id).first()

    formatted_devices = [device.format() for device in devices]

    start = (page - 1) * 10
    end = start + limit

    return {
        "success": True,
        "brand": brand.format(),
        "devices": formatted_devices[start:end],
    }


@app.get("/devices/{device_id}")
async def get_device_specifications(device_id):
    specs = db_session.query(DeviceSpecification).filter_by(device_id=device_id)

    device = db_session.query(Device).filter_by(id=device_id).first()
    brand = device.brand.format()

    grouped_specs = {}
    for spec in specs:
        spec_category = spec.spec_category
        specification = spec.specification
        spec_value = spec.spec_value
        grouped_specs.setdefault(spec_category, {})

        grouped_specs[spec_category][specification] = spec_value

    return {
        "success": True,
        "brand": brand,
        "device": device,
        "specifications": grouped_specs,
    }


@app.get("/devices")
async def all_devices(page: int = 1, limit: int = 10):
    devices = db_session.query(Device).all()

    formatted_devices = [device.format() for device in devices]

    start = (page - 1) * 10
    end = start + limit

    return {
        "success": True,
        "devices": formatted_devices[start:end],
        "total_devices": len(formatted_devices),
    }


@app.get("/latest_devices")
async def latest_devices():
    pass


@app.get("/in_stores_now")
async def in_stores_now():
    pass


@app.get("/top")
async def top():
    pass


@app.get("/search")
async def search():
    pass
