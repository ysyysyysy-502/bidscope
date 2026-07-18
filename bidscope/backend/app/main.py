from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import router

app = FastAPI(title="BidScope 标讯罗盘 API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "name": "BidScope / 标讯罗盘",
        "message": "多源标讯检索、证据去重、增量账本与 Word 交付 Demo",
        "docs": "/docs",
    }
