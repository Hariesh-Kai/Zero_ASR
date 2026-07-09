from fastapi import APIRouter

from services.company_search import CompanySearchService

router = APIRouter()

service = CompanySearchService()


@router.get("/")
def search_company(query: str):

    return service.search(query)