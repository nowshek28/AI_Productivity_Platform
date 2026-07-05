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

        # Sanitize path to prevent log injection via CRLF characters
        safe_path = request.url.path.replace("\r", "").replace("\n", "")
        logger.info(
            "%s %s | %s | %.2f ms",
            request.method,
            safe_path,
            response.status_code,
            process_time,
        )

        # Security headers (OWASP A05 - Security Misconfiguration)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Cache-Control"] = "no-store"

        return response