from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    owner_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


class ProductSchema(BaseModel):
    name: str
    description: str
    price: float
