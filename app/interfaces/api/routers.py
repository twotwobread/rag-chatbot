from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from app.rag.chains import get_chain
from app.schemas.chat import ChatRequest
from app.schemas.query import QueryRequest, QueryResponse
from app.services.qa_service import QAService

router = APIRouter(prefix="/chats")


@router.post(
    "/query",
    response_model=QueryResponse,
    summary="쿼리 응답 API",
    description="RAG 기반으로 단순하게 쿼리에 대한 응답을 하는 API",
)
async def query(request: QueryRequest, chain=Depends(get_chain)):
    qa_service = QAService(chain)
    return qa_service.query(request.query)


@router.post(
    "/chat",
    response_class=StreamingResponse,
    summary="채팅 응답 API",
    description="RAG 기반으로 history를 반영한 채팅 API",
)
async def chat(request: ChatRequest, chain=Depends(get_chain)):
    qa_service = QAService(chain)
    return StreamingResponse(
        qa_service.chat(request.query, request.session_id),
        media_type="text/plain",
    )
