from fastapi import FastAPI

from api.routes.search import router as search_router
from api.routes.company import router as company_router
from api.routes.advisor import router as advisor_router
from api.routes.technical import router as technical_router
from api.routes.news import router as news_router
from fastapi.middleware.cors import CORSMiddleware
from api.routes.chart import router as chart_router 
from api.routes.financials import router as financials_router

app = FastAPI(
    title="AI Stock Advisor API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------
# Company Analysis
# ---------------------------------------

app.include_router(
    company_router,
    prefix="/company",
    tags=["Company"]
)

# ---------------------------------------
# Search
# ---------------------------------------

app.include_router(
    search_router,
    prefix="/search",
    tags=["Search"]
)

# ---------------------------------------
# AI Advisor
# ---------------------------------------

app.include_router(
    advisor_router,
    prefix="/advisor",
    tags=["Advisor"]
)

app.include_router(
    technical_router,
    prefix="/technical",
    tags=["Technical"]
)

app.include_router(
    chart_router,
    prefix="/chart",
    tags=["Chart"],
)

app.include_router(
    news_router,
    prefix="/news",
    tags=["News"]
)

app.include_router(

    financials_router,

    prefix="/financials",

    tags=["Financials"],

)

# ---------------------------------------
# Home
# ---------------------------------------

@app.get("/")
def home():

    return {

        "status": "running",

        "project": "AI Stock Advisor",

        "version": "1.0.0",

        "available_endpoints": [

            "/company/{ticker}",

            "/advisor/{ticker}",

            "/search",

            "/docs",

        ]

    }