from dotenv import load_dotenv
from fastapi import FastAPI

from src.routers.downloader import router as downloader_router
from src.routers.media import router as media_router
from src.routers.frontend import router as frontend_router

load_dotenv()

def create_app() -> FastAPI:
    app = FastAPI(title="API Downloader")

    # Rotas
    app.add_api_route("/health", lambda: {"message": "The API is up and running!"})
    app.include_router(frontend_router)
    app.include_router(downloader_router)
    app.include_router(media_router)

    return app
