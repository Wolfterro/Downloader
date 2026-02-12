import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter(prefix="/media", tags=["media"])
MEDIA_DIR = Path("media")

# GET
# ---
@router.get("/{filename}")
async def filename(filename: str):
    """
    Retorna o arquivo baixado.

    Parâmetros:
    - filename: str

    Retorna:
    - FileResponse
    """
    file_path = MEDIA_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )
