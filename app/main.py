import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.core.config import settings
from app.interfaces.api.routers import router
from app.storage.vectorstore import init_vectorstore


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_vectorstore()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="health 체크",
    description="health 체크",
)
def health():
    return HealthResponse(status="healthy")


if __name__ == "__main__":
    if settings.APP_MODE == "ui":
        print("Starting in streamlit server...")
        os.execvp(
            "python",
            [
                "python",
                "-m",
                "streamlit",
                "run",
                "app/interfaces/ui.py",
                "--server.port",
                str(settings.PORT),
            ],
        )
    else:
        print("Starting in fastapi server...")
        uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
