import pydantic


class Response(pydantic.BaseModel):
    success: bool = True


class PaginatedResponse(Response):
    page: int
    size: int


class BrandNoNum(pydantic.BaseModel):
    id: str
    name: str
    url: str

    class Config:
        orm_mode = True


class Brand(BrandNoNum):
    num_devices: int


class DeviceNoBrandID(pydantic.BaseModel):
    id: str
    name: str
    url: str
    thumbnail: str
    summary: str

    class Config:
        orm_mode = True


class Device(DeviceNoBrandID):
    brand_id: str


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
    brand: BrandNoNum
    devices: list[DeviceNoBrandID]


class DeviceSpecDetail(Response):
    brand: BrandNoNum
    device: DeviceNoBrandID
    specifications: dict
