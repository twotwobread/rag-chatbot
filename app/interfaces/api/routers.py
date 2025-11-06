from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from app.rag.chatbot import RAGChatbot, get_rag_chatbot
from app.schemas.chat import ChatRequest
from app.schemas.query import QueryRequest, QueryResponse

router = APIRouter()


@router.post(
    "/query",
    response_model=QueryResponse,
    summary="쿼리 응답 API",
    description="RAG 기반으로 단순하게 쿼리에 대한 응답을 하는 API",
)
async def query(
    request: QueryRequest, chatbot: RAGChatbot = Depends(get_rag_chatbot)
):
    return chatbot.ask(request.query)


@router.post(
    "/chat",
    response_class=StreamingResponse,
    summary="채팅 응답 API",
    description="RAG 기반으로 history를 반영한 채팅 API",
)
async def chat(
    request: ChatRequest, chatbot: RAGChatbot = Depends(get_rag_chatbot)
):
    return StreamingResponse(
        chatbot.ask_stream(request.query, request.session_id),
        media_type="text/plain",
    )
