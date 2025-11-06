from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.core import database_client
from src.api import api_router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database_client.create_tables()

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(GZipMiddleware, minimum_size=50)

app.include_router(api_router)


@app.get("/health")
async def health():
    return {"status": "ok"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Морской бой",
        version="0.0.1",
        description="API для морского боя на FastAPI + PostgresSQL",
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
