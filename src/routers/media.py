import datetime
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

import urllib

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

@router.get('/api/list')
async def list_files() -> dict:
    files = []
    for file in MEDIA_DIR.iterdir():
        if (file.name.startswith(".")):
            continue

        hostname = os.environ.get("HOSTNAME")
        filename_quoted = urllib.parse.quote(file.name)
        created_at = datetime.datetime.fromtimestamp(file.stat().st_ctime)
        
        # Arquivo será removido em hora cheia (ex: 17:00:00).
        # Se o arquivo tiver sido baixado às 16:38:00, 
        # ele será removido às 17:00:00, isto é, será deletado em 22 minutos.
        now = datetime.datetime.now()
        now_minute = now.minute

        file_dict = {
            "name": file.name,
            "url": f"{hostname}/media/{filename_quoted}",
            "size": str(file.stat().st_size),
            "size_mb": f'{file.stat().st_size / 1000 / 1000:.2f}', # MB
            "created_at": created_at,
            "minutes_remaining": 60 - now_minute
        }

        files.append(file_dict)
    
    return {
        "files": files
    }