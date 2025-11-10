from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    tax_rate = Column(Float, default=0.0)  # e.g., 16.0 for 16%

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    total = Column(Float, nullable=False)
    tax = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    items_json = Column(JSON, nullable=False)  # list of {product_id, qty, price, tax_rate}

class InvoiceLog(Base):
    __tablename__ = "invoice_logs"
    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"))
    request_json = Column(JSON, nullable=False)
    response_json = Column(JSON, nullable=False)
    status = Column(String, index=True)  # SUCCESS / FAILED
    created_at = Column(DateTime, default=datetime.utcnow)
    sale = relationship("Sale")
