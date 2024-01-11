"""FastAPI Server Setup"""
from datetime import datetime
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import environment
from .routes import user_router, products_router


allowed_methods = ["POST, GET", "DELETE", "PUT", "PATCH"]

tags_metadata = [
    {
        "name": "E-commerce API",
        "description": "A set of endpoints to to register and manage e-commerce data",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=allowed_methods,
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(products_router)

@app.get("/", status_code=HTTPStatus.OK)
def root():
    return "E-commerce Application API"


@app.on_event("startup")
def startup_event():
    print(f"{datetime.now()} - Starting up server...")


@app.on_event("shutdown")
def shutdown_event():
    print(f"{datetime.now()} - Shutting down server...")
