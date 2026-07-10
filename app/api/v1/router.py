from fastapi import APIRouter

from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.todos import router as todos_router
from app.api.v2.routes.transcript import router as transcript_router

router = APIRouter()

# Take all the routes from health_router and register them under /api/v1
# the final url for the health check endpoint will be /api/v1/health
router.include_router(
    health_router, 
    prefix="/api/v1",
    tags=["health"],
    )

# Take all the routes from todos_router and register them under /api/v1
# the final url for the todos endpoint will be /api/v1/todos
router.include_router(
    todos_router,
    prefix="/api/v1",
    tags=["todos"],
)
