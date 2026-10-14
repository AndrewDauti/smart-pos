from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    sku: str
    name: str
    price: float
    tax_rate: float = 0.0
    category: str = "Plates"


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

    class Config:
        from_attributes = True


class CartItem(BaseModel):
    product_id: int
    qty: int = Field(gt=0)


class SaleCreate(BaseModel):
    items: list[CartItem] = Field(min_length=1)
    discount: float = Field(default=0.0, ge=0)


class SaleRead(BaseModel):
    id: int
    total: float
    tax: float
    discount: float
    items_json: list
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class InvoiceSubmission(BaseModel):
    sale_id: int


class InvoiceLogRead(BaseModel):
    id: int
    sale_id: int
    status: str
    response_json: dict

    class Config:
        from_attributes = True
