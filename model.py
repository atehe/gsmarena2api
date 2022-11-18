from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, Session

Base = declarative_base()

DATABASE_URI = "sqlite+pysqlite:///gsmarena.db"


class Brand(Base):
    __tablename__ = "brand"

    id = Column(String(), primary_key=True)
    name = Column(String())
    url = Column(String())
    num_devices = Column(Integer())
    devices = relationship("Device", back_populates="brand")

    def insert(self):
        db_session.add(self)
        db_session.commit()

    def update(self):
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "num_devices": self.num_devices,
        }


class Device(Base):
    __tablename__ = "device"

    id = Column(String(), primary_key=True)
    brand_id = Column(ForeignKey("brand.id"))
    name = Column(String())
    url = Column(String())
    thumbnail = Column(String())
    summary = Column(String())

    brand = relationship("Brand", back_populates="devices")
    specs = relationship("DeviceSpecification", back_populates="device")

    def insert(self):
        db_session.add(self)
        db_session.commit()

    def update(self):
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def format(self):
        return {
            "id": self.id,
            "brand_id": self.brand_id,
            "name": self.name,
            "url": self.url,
            "thumbnail": self.thumbnail,
            "summary": self.summary,
        }


class DeviceSpecification(Base):
    __tablename__ = "device_specification"

    device_id = Column(ForeignKey("device.id"))
    spec_id = Column(Integer, primary_key=True, nullable=False)
    spec_category = Column(String())
    specification = Column(String())
    spec_value = Column(String())

    device = relationship("Device", back_populates="specs")

    def insert(self):
        db_session.add(self)
        db_session.commit()

    def update(self):
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def format(self):
        return {
            "device_id": self.device_id,
            "spec_category": self.spec_category,
            "specification": self.specification,
            "spec_value": self.spec_value,
        }


def __init__db():
    engine = create_engine(DATABASE_URI, future=True)
    Base.metadata.create_all(engine)
    db_session = Session(engine)

    return db_session


db_session = __init__db()
