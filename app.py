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

    return 200


@app.get("/brands")
async def get_brands():
    brands = db_session.query(Brand).all()

    formatted_brands = [brand.format() for brand in brands]

    return formatted_brands


@app.get("/brands/{brand_id}")
async def get_devices(brand_id):
    devices = db_session.query(Device).filter_by(brand_id=brand_id)

    formatted_devices = [device.format() for device in devices]

    # TODO: get brand details and add to endpoint output

    return formatted_devices


@app.get("/devices/{device_id}")
async def get_device_specifications(device_id):
    specs = db_session.query(DeviceSpecification).filter_by(device_id=device_id)

    formatted_specs = [spec.format() for spec in specs]

    # TODO: get device, brand details and add to endpoint output

    return formatted_specs


@app.get("/devices")
async def devices():
    devices = db_session.query(Device).all()

    formatted_devices = [devices.format() for device in devices]

    # TODO: get brand details and add to endpoint output

    return formatted_devices


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
