from fastapi import APIRouter
from api.app.api.v1.endpoints import parsing

api_router = APIRouter()
api_router.include_router(parsing.router, prefix="/parsing", tags=["parsing"])
