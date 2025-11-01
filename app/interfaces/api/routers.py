from fastapi import APIRouter, Depends

from app.rag.chains import get_chain
from app.schemas.query import QueryRequest, QueryResponse
from app.services.qa_service import QAService

router = APIRouter(prefix="/chats")


@router.post(
    "/query",
    response_model=QueryResponse,
    summary="쿼리 응답 API",
    description="RAG 기반으로 단순하게 쿼리에 대한 응답을 하는 API",
)
def query(request: QueryRequest, chain=Depends(get_chain)):
    qa_service = QAService(chain)
    return qa_service.query(request.query)
