from fastapi import FastAPI

from routers.user_router import router as router_users
from routers.transaction_router import router as router_transactions

from fastapi.middleware.cors import CORSMiddleware

mi_app = FastAPI()

mi_app.include_router(router_users)
mi_app.include_router(router_transactions)


origins = [
    "http://localhost.tiangolo.com", "https://localhost.tiangolo.com",
    "http://localhost", "http://localhost:8080", "https://cajero-app-frontend-123.herokuapp.com"
]
mi_app.add_middleware(
    CORSMiddleware, allow_origins=origins,
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)
