from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    """
    Health check endpoint. Check if the API is running and healthy.
    """
    return {"status": "healthy"}