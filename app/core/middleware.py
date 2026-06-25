import logging
import time

from fastapi import FastAPI, Request

logger = logging.getLogger(__name__)


def register_middleware(app:FastAPI) -> None:
    """
    Register middleware for the FastAPI application.
    """

    @app.middleware("http")
    async def log_request(request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = (time.perf_counter() - start_time) * 1000  # Convert to milliseconds
        logger.info(
            "%s %s | %s | %.2f ms",
            request.method,
            request.url.path,
            response.status_code,
            process_time,
        )
        
        return response