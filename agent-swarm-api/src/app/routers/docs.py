import starlette.status as status
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

docs_router = APIRouter()


@docs_router.get("/", include_in_schema=False)
async def redirect_to_docs(request: Request):
    """
    Redirect root URL to the API documentation.
    """
    docs_url = request.url_for("swagger_ui_html")
    return RedirectResponse(url=docs_url, status_code=status.HTTP_302_FOUND)
