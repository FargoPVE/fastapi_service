import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from redis import asyncio as aioredis
from sqladmin import Admin
from prometheus_fastapi_instrumentator import Instrumentator, metrics
import sentry_sdk

from app.api.v1.api import base_router
from app.core.admin_auth import authentication_backend
from app.core.admin_views import BookingAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.core.config import settings
from app.db.session import engine
from app.pages.base import router
from app.utils.logger import logger

app = FastAPI(
    title="Booking",
    version="0.1.0",
    description="Booking project",
    root_path="/api",
)

if settings.MODE != "TEST":
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

app.include_router(router=base_router)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                    "Authorization"],
)

app = VersionedFastAPI(app,
    version_format="{major}",
    prefix_format="/api/v{major}",
    description="Booking project",
)
app.include_router(router=router)

if settings.MODE == "TEST":
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")

@app.on_event("startup")
def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")

instrumentator = Instrumentator(
    # should_group_status_codes=False,
    # should_ignore_untemplated=True,
    # should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=[".*admin.*", "/metrics"],
    # env_var_name="ENABLE_METRICS",
    # inprogress_name="inprogress",
    # inprogress_labels=True,
)
instrumentator.instrument(app).expose(app)


admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(BookingAdmin)

app.mount("/static", StaticFiles(directory="app/static"), "static")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info("Request execution time", extra={
        "process_time": round(process_time, 4)
    })
    return response
