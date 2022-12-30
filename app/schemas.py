import pydantic


class Response(pydantic.BaseModel):
    success: bool = True


class PaginatedResponse(Response):
    page: int
    size: int


class Brand(pydantic.BaseModel):
    id: str
    name: str
    url: str
    num_devices: int

    class Config:
        orm_mode = True


class Device(pydantic.BaseModel):
    id: str
    brand_id: str
    name: str
    url: str
    thumbnail: str
    summary: str

    class Config:
        orm_mode = True


class DeviceWithSpec(Device):
    specs: dict


class BrandsResponse(PaginatedResponse):
    brands: list[Brand]
    total_brands: int

    class Config:
        orm_mode = True


class DevicesResponse(PaginatedResponse):
    total_devices: int
    devices: list[Device]


class BrandDevicesResponse(DevicesResponse):
    brand: Brand


class DeviceSpecDetail(Response):
    brand: Brand
    device: Device
    specifications: dict