import logging

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.database import get_db
from app.schemas import(
    LoadProcedureResponse,
    ProductCreate,
    ProductCuratedResponse,
    ProductIngestionResponse
)

router = APIRouter(prefix="/products", tags=["products"])
logger = logging.getLogger(__name__)

@router.post("/ingest",response_model = ProductIngestionResponse, status_code=201)

def ingest_products(
        products: list[ProductCreate],
        source_system: str = Header(default="manual-api"),
        db: Session = Depends(get_db)
):
    try:
        logger.info(f"API called | endpoint=/products/ingest | records = {len(products)}")

        batch_id = crud.insert_products_staging(
            db=db,
            products=products,
            source_system=source_system
        )

        return {
            "message": "Products inserted into staging successfully",
            "inserted_records": len(products),
            "batch_id": batch_id,
        }

    except Exception as error:
        logger.exception(f"failed product ingestion | error={str(error)}")
        raise HTTPException(status_code=500, detail="Product ingestion failed")

@router.post("/load",response_model = LoadProcedureResponse)
def load_products(db:Session = Depends(get_db)):
    try:
        logger.info(f"API called | endpoint=/products/load")
        crud.run_load_products_procedure(db)
        return {"message":"Stored procedure executed successfully"}

    except Exception as error:
        logger.exception(f"Stored procedure failed | error={str(error)}")
        raise HTTPException(status_code=500, detail="Stored procedure execution failed")

@router.get("/curated", response_model = list[ProductCuratedResponse])
def get_products(db: Session = Depends(get_db)):
    try:
        logger.info(f"API called | endpoint=/products/curated")

        return crud.get_curated_products(db)

    except Exception as error:
        logger.exception(f"failed fetching curated products | error={str(error)}")
        raise HTTPException(status_code=500, detail="failed fetching curated products")