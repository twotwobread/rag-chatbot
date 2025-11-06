from typing import Generator

from app.rag.chains import RAGChain
from app.schemas.query import QueryResponse


class QAService:
    def __init__(self, chain: RAGChain):
        self.chain = chain

    def query(self, text: str) -> QueryResponse:
        return self.chain.query(text)

    def chat(self, text: str, session_id: str) -> Generator[str, None, None]:
        return self.chain.chat(text, session_id)
