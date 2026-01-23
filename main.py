from typing import Union
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from starlette_csrf.middleware import CSRFMiddleware

def get_app() -> FastAPI:
    middleware = [
        Middleware(
            GZipMiddleware,
            minimum_size=1000,
            compresslevel=5
        ),
        Middleware(
            CORSMiddleware,
            allow_methods=['GET'],
            allow_origins=['*']
        ),
        Middleware(
            CSRFMiddleware,
            secret="__CHANGE_ME__"
        )
    ]
    app = FastAPI(
        root_path=Configuration,
        middleware=middleware
    )
    return app

app = get_app()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
