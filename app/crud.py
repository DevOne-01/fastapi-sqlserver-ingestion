import logging
from uuid import uuid4
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.models import ProductCurated,ProductStaging
from app.schemas import ProductCreate

logger = logging.getLogger(__name__)


def insert_products_staging(db:Session, products: list[ProductCreate], source_system: str):
    batch_id = str(uuid4())

    logging.info(f"Starting staging insert | batch_id = {batch_id} | records = {len(products)}")

    staging_rows = [
        ProductStaging(
            name=product.name,
            price=product.price,
            category=product.category,
            source_system=source_system,
            batch_id=batch_id,
        )
        for product in products
    ]

    db.add_all(staging_rows)
    db.commit()

    logger.info(f"Complete staging insert | batch_id = {batch_id} | records = {len(products)}")

    return batch_id

def run_load_products_procedure(db:Session):
    logger.info("Starting stored procedure execution | procedure.usp_load_products")

    db.execute(text("EXEC curated.usp_load_products"))
    db.commit()

    logger.info("Completed stored procedure execution | procedure = curated.usp_load_products")

def get_curated_products(db:Session):
    logger.info("Fetching curated products")

    return db.query(ProductCurated).order_by(ProductCurated.product_id.desc()).all()