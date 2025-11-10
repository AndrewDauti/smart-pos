from pydantic import BaseModel, Field
from typing import List, Optional

class ProductBase(BaseModel):
    sku: str
    name: str
    price: float
    tax_rate: float = 0.0

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
    items: List[CartItem]
    discount: float = 0.0

class SaleRead(BaseModel):
    id: int
    total: float
    tax: float
    discount: float
    items_json: list
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
