from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship

from .database import db_session, engine

Base = declarative_base()


class BaseModel:
    id = Column(String(), primary_key=True)

    def insert(self):
        db_session.add(self)
        db_session.commit()

    def update(self, **kwargs):
        db_session.query(self.__class__) \
            .filter(self.__class__.id == self.id) \
            .update(kwargs)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def format(self):
        raise NotImplementedError("Method not implemented")


class Brand(Base, BaseModel):
    __tablename__ = "brand"

    name = Column(String())
    url = Column(String())
    num_devices = Column(Integer())
    devices = relationship("Device", back_populates="brand")

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "num_devices": self.num_devices,
        }


class Device(Base, BaseModel):
    __tablename__ = "device"

    brand_id = Column(ForeignKey("brand.id"))
    name = Column(String())
    url = Column(String())
    thumbnail = Column(String())
    summary = Column(String())

    brand = relationship("Brand", back_populates="devices")
    specs = relationship("DeviceSpecification", back_populates="device")

    def format(self):
        return {
            "id": self.id,
            "brand_id": self.brand_id,
            "name": self.name,
            "url": self.url,
            "thumbnail": self.thumbnail,
            "summary": self.summary,
        }


class DeviceSpecification(Base, BaseModel):
    __tablename__ = "device_specification"

    id = None
    device_id = Column(ForeignKey("device.id"))
    spec_id = Column(Integer, primary_key=True, nullable=False)
    spec_category = Column(String())
    specification = Column(String())
    spec_value = Column(String())

    device = relationship("Device", back_populates="specs")

    def update(self, **kwargs):
        db_session.query(self.__class__) \
            .filter(self.__class__.spec_id == self.spec_id) \
            .update(kwargs)
        db_session.commit()

    def format(self):
        return {
            "device_id": self.device_id,
            "spec_category": self.spec_category,
            "specification": self.specification,
            "spec_value": self.spec_value,
        }

Base.metadata.create_all(engine)
