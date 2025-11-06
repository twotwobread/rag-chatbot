from typing import Iterator

from app.rag.chains import RAGChain, get_chain
from app.schemas.query import QueryResponse


class RAGChatbot:
    def __init__(self, chain: RAGChain):
        self.chain = chain

    def ask(self, question: str) -> QueryResponse:
        return self.chain.query(question)

    def ask_stream(self, question: str, session_id: str) -> Iterator[str]:
        return self.chain.chat(question, session_id)


def get_rag_chatbot():
    return RAGChatbot(chain=get_chain())
