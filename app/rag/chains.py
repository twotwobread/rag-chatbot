from operator import itemgetter

from langchain_core.runnables import RunnablePassthrough

from app.core.llms import llm
from app.rag.prompts import get_rag_prompt
from app.schemas.query import QueryResponse
from app.storage.vectorstore import get_retriever


class RAGChain:
    def __init__(self):
        self.llm = llm
        self.prompt = get_rag_prompt()
        self.retriever = get_retriever()

        self.query_chain = (
            {
                "context": itemgetter("question") | self.retriever,
                "question": RunnablePassthrough(),
            }
            | self.prompt
            | self.llm
        )
        self.stream_chain = None

    def query(self, text: str) -> QueryResponse:
        ai_message = self.query_chain.invoke({"question": text})

        return QueryResponse(answer=ai_message.content)


def get_chain() -> RAGChain:
    return RAGChain()
