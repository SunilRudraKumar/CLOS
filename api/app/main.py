from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.app.core.config import settings

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # Set all CORS enabled origins
    if settings.ALLOWED_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"], # For dev simplicity, refine in prod
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.get("/health")
    def health_check():
        return {"status": "ok", "project": settings.PROJECT_NAME}

    @app.get("/")
    def root():
        return {"message": "Welcome to CLOS API - The Logistics Data Firewall"}

    # Include routers
    from api.app.api.v1.api import api_router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.app.main:app", host="0.0.0.0", port=8000, reload=True)
