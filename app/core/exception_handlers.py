import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.todo import TodoNotFoundError

logger = logging.getLogger(__name__)

def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all custom exception handlers.
    """

    @app.exception_handler(TodoNotFoundError)
    async def todo_not_found_handler(request: Request, exc: TodoNotFoundError):
        """
        Handle TodoNotFoundError exceptions.
        """
        logger.warning(str(exc))

        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )