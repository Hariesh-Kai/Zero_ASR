from fastapi import FastAPI
from api.routes.search import router as search_router
from api.routes.company import router as company_router

app = FastAPI(
    title="AI Stock Advisor API",
    version="1.0.0"
)

app.include_router(
    company_router,
    prefix="/company",
    tags=["Company"]
)

app.include_router(
    search_router,
    prefix="/search",
    tags=["Search"]
)

@app.get("/")
def home():
    return {
        "status": "running",
        "project": "AI Stock Advisor"
    }