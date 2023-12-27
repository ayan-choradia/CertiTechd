from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.api.router import router
from src.config import settings
from src.logging.config import LOGGING_CONFIG
from src.logging.utils import configure_logging

configure_logging()

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)
app.mount("/api/v1/static", StaticFiles(directory="./static"), name="static")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=[str(origin) for origin in settings.BACK
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.include_router(router, prefix=settings.API_V1_STR)
add_pagination(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        reload=settings.RELOAD,
        workers=8,
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING_CONFIG,
        access_log=False,
    )
