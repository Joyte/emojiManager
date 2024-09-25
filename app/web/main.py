from fastapi import FastAPI, Request, staticfiles, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.web.extensions.apimodels import pagecontent

app = FastAPI()
templates = Jinja2Templates(directory="app/web/templates")

pages = APIRouter(
    prefix="",
    tags=["Pages API"],
)


@pages.get("/api/page/{page}")
async def get_page(page: pagecontent, request: Request):
    return templates.TemplateResponse(
        f"pages/{page.value}.j2",
        {
            "request": request,
        },
    )


@pages.get("/")
async def redirect():
    """
    Redirect to the home page.
    """
    return RedirectResponse(url="/page/home")


@pages.get("/page/{page}")
async def index(request: Request):
    return templates.TemplateResponse(
        "index.j2",
        {"request": request},
    )


# Add error handling for any exceptions
@app.exception_handler(500)
@app.exception_handler(StarletteHTTPException)
async def exception_handler(request: Request, exc: StarletteHTTPException):
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            content={
                "code": getattr(exc, "status_code", 500),
                "message": getattr(exc, "detail", "Internal Server Error"),
            },
            status_code=getattr(exc, "status_code", 500),
        )

    return templates.TemplateResponse(
        "error.j2",
        {
            "request": request,
            "code": getattr(exc, "status_code", 500),
            "message": getattr(exc, "detail", "Internal Server Error"),
        },
        status_code=getattr(exc, "status_code", 500),
    )


app.include_router(pages)
app.mount("/", staticfiles.StaticFiles(directory="app/web/public"), name="public")


def run_web():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
