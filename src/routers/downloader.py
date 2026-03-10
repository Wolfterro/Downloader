import os
from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool

from src.core.utils import isValidUrl
from src.schemas.downloader import DownloaderFileSchema
from src.services.downloader import DownloaderService

router = APIRouter(prefix="/downloader", tags=["downloader"])


# POST
# ----
@router.post("/download", response_model=dict)
async def download_file(body: DownloaderFileSchema) -> dict:
    """
    Recebe o pedido de download.

    Parâmetros:
    - body: DownloaderFileSchema

    Retorna:
    - dict: Dicionário com chave "success" e link para baixar o arquivo.
    """
    if not isValidUrl(body.url):
        raise HTTPException(status_code=400, detail="URL inválida")

    downloader = DownloaderService(body)
    download_url = await run_in_threadpool(downloader.download)

    hostname = os.environ.get("HOSTNAME")
    download_url = f"{hostname}/{download_url}"

    return {"success": True, "url": download_url}
