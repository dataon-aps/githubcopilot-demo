from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from FastApi.routers.router_departure import router as departure_router
from FastApi.helpers.database import init_db

App = FastAPI(
    title="Train Timetable API",
    description="A simple API for querying train departure times.",
    version="1.0.0",
)

App.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

App.include_router(departure_router, prefix="/api")

init_db()
