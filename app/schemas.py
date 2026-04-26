from decimal import Decimal
from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    price: Decimal = Field(..., gt=0)
    category: str = Field(..., min_length=2, max_length=100)


class ProductIngestionResponse(BaseModel):
    message: str
    inserted_records: int
    batch_id: str

class ProductCuratedResponse(BaseModel):
    product_id: int
    name: str
    price: Decimal
    category: str

    class Config:
        from_attributes = True


class LoadProcedureResponse(BaseModel):
    message: str