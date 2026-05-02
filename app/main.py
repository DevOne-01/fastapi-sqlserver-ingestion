import logging
import time
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from uvicorn import middleware

from app.logging_config import setup_logging
from app.routers import products

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title="FastAPI SQL Server Ingestion Project",
    version="1.0.0",
)

app.include_router(products.router)

@app.middleware("http")

async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()

    logger.info(f"Request started | request_id={request_id} | method={request.method} | path = {request.url.path}| {time.time() - start_time}")

    try:
        response = await call_next(request)
        execution_time_ms = round((time.time()-start_time)*1000,2)

        logger.info(
            f"Request completed | request_id={request_id} | method={request.method}"
            f"| path={request.url.path} | status_code={response.status_code} | execution_time_ms={execution_time_ms}"
        )

        response.headers["X-Request-ID"] = request_id
        return response
    except Exception as error:
        execution_time_ms = round((time.time() - start_time) * 1000, 2)

        logger.exception(
            f"Request failed | request_id={request_id} | method={request.method} "
            f"| path={request.url.path} | execution_time_ms={execution_time_ms} | error={str(error)}"
        )

        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "request_id": request_id},
        )

    @app.get("/")
    def health_check():
        logger.info("Health check endpoint called")
        return {"status": "running"}