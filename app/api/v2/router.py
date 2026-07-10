from fastapi import APIRouter

from app.api.v2.routes.transcript import router as transcript_router

router = APIRouter()


# Take all the routes from transcript_router and register them under /api/v2
# the final url for the transcript endpoint will be /api/v2/todos
router.include_router(
    transcript_router,
    prefix="/api/v2",
    tags=["transcripts"],
)