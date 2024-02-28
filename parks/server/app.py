# from database import session

import logging
from importlib.metadata import version

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

# from config import config

__version__ = version("parks")

from .uvicorn_logging import setup_logging

logger = logging.getLogger("MainApp")

app = FastAPI(title="PARKS API", version=__version__)

### MIDDLEWARE ###
origins = [
    "http://localhost:8080",
]


# REF: https://github.com/tiangolo/fastapi/issues/775
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        # logging.exception(e)
        return Response("Internal server error", status_code=500)


# This should come before CORSMiddleware is added
app.middleware("http")(catch_exceptions_middleware)

# add CORS origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.get("/", response_class=HTMLResponse)
async def root():
    """

    Returns:
        A block of HTML to use as the root containing the title and the version

    """
    return f"""
    <html>
        <head>
            <title>{app.title}</title>
        </head>
        <body>
            <h1>{app.title}</h1>
            <i>Version: {__version__}</i>
        </body>
    </html>
    """


### ROUTERS ###
from .routers import v1

app.include_router(v1.router, prefix="/v1")

