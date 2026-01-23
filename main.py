from typing import Union, Tuple
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.middleware.gzip import GZipMiddleware
from starlette_csrf.middleware import CSRFMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

def rate_limit_handler(request: Request, exc: Exception) -> Response:
    assert isinstance(exc, RateLimitExceeded)
    return _rate_limit_exceeded_handler(request, exc)

def get_app() -> Tuple[FastAPI, Limiter]:
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
    limiter = Limiter(key_func=get_remote_address)
    app = FastAPI(
        # root_path=Configuration,
        middleware=middleware,
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
    return app, limiter

app, limiter = get_app()


@app.get("/")
@limiter.limit("1/minute")
def read_root(request: Request):
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
