from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from .database import Base
from .timeutil import now_lusaka


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    category = Column(String, nullable=False, default="Plates")
    price = Column(Float, nullable=False)
    tax_rate = Column(Float, default=0.0)  # e.g., 16.0 for 16%


class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=now_lusaka)
    total = Column(Float, nullable=False)
    tax = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    items_json = Column(JSON, nullable=False)
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")


class SaleItem(Base):
    __tablename__ = "sale_items"
    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"), nullable=True)
    sku = Column(String)
    name = Column(String)
    qty = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    tax_rate = Column(Float, nullable=False, default=0.0)
    line_subtotal = Column(Float, nullable=False)
    line_tax = Column(Float, nullable=False)
    line_total = Column(Float, nullable=False)
    sale = relationship("Sale", back_populates="items")


class InvoiceLog(Base):
    __tablename__ = "invoice_logs"
    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"))
    request_json = Column(JSON, nullable=False)
    response_json = Column(JSON, nullable=False)
    status = Column(String, index=True)  # SUCCESS / FAILED
    created_at = Column(DateTime, default=now_lusaka)
    sale = relationship("Sale")
