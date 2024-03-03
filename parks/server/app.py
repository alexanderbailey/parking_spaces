import logging
import os
from importlib.metadata import version
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from .uvicorn_logging import setup_logging
from .routers import v1

__version__ = version("parks")
app = FastAPI(title="PARKS API", version=__version__)


# REF: https://github.com/tiangolo/fastapi/issues/775
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logging.exception(e)
        return Response("Internal server error", status_code=500)


# This should come before CORSMiddleware is added
app.middleware("http")(catch_exceptions_middleware)

# MIDDLEWARE
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

logger = logging.getLogger("MainApp")


@app.on_event("startup")
async def startup():
    setup_logging()


project_dir = os.path.dirname(__file__)
template_dir = os.path.join(project_dir, "frontend/templates")
static_dir = os.path.join(project_dir, "frontend/static")
templates = Jinja2Templates(directory=template_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "version": __version__,
        "title": "PARKS",
        "request": request
    })


# ROUTERS
app.include_router(v1.router, prefix="/v1")

