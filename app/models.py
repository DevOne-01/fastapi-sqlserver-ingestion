from sqlalchemy import Column, DateTime, Integer, Numeric, String, func
from app.database import Base

class ProductStaging(Base):
    __tablename__ = "products_staging"
    __table_args__ = {"schema": "raw"}

    staging_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    category = Column(String(100), nullable=False)
    source_system = Column(String(100), nullable=True)
    batch_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class ProductCurated(Base):
    __tablename__ = "products"
    __table_args__ = {"schema": "curated"}

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    category = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, nullable=True)

class ApiLog(Base):
    __tablename__ = "api_logs"
    __table_args__ = {"schema": "audit"}

    log_id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String(100))
    endpoint = Column(String(255))
    method = Column(String(20))
    status_code = Column(Integer)
    message = Column(String(1000))
    created_at = Column(DateTime, server_default=func.now())