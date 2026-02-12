from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="", tags=["Frontend"])


# GET
# ---
@router.get("/", response_model=dict)
async def root():
    """
    Frontend da aplicação.

    Parâmetros:
    - Nenhum.

    Retorna:
    - HTMLResponse: HTML.
    """

    content = open("content/index.html", "r").read()
    return HTMLResponse(
        content=content,
        status_code=200
    )