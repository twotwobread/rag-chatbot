from typing import Annotated, Iterator, NotRequired, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from app.core.llms import llm
from app.rag.prompts import get_qa_prompt, get_stream_prompt
from app.schemas.query import QueryResponse
from app.storage.vectorstore import get_retriever


class RAGState(TypedDict):
    messages: Annotated[list, add_messages]
    question: str
    context: list
    prompt_text: NotRequired[str]


class RAGChain:
    def __init__(self):
        self.llm = llm
        self.retriever = get_retriever()
        self.memory = MemorySaver()

        self.query_graph = self._build_query_graph()

        self.chat_graph = self._build_chat_graph()

    def _build_query_graph(self):
        workflow = StateGraph(RAGState)

        workflow.add_node("retrieve", self._retrieve_documents)
        workflow.add_node("generate", self._generate_answer)

        workflow.add_edge(START, "retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)

        return workflow.compile()

    def _retrieve_documents(self, state: RAGState):
        question = state["question"]
        docs = self.retriever.invoke(question)

        return {"context": docs}

    def _generate_answer(self, state: RAGState):
        prompt = get_qa_prompt()

        # 프롬프트에 context와 question 주입
        messages = prompt.invoke(
            {
                "context": "\n\n".join(
                    [doc.page_content for doc in state["context"]]
                ),
                "question": state["question"],
            }
        )

        response = self.llm.invoke(messages)

        return {"messages": [response]}

    def _build_chat_graph(self):
        workflow = StateGraph(RAGState)

        workflow.add_node("retrieve", self._retrieve_documents)
        workflow.add_node("prepare-prompt", self._prepare_stream_prompt)

        workflow.add_edge(START, "retrieve")
        workflow.add_edge("retrieve", "prepare-prompt")
        workflow.add_edge("prepare-prompt", END)

        return workflow.compile(checkpointer=self.memory)

    def _prepare_stream_prompt(self, state: RAGState):
        # 이전 메시지들 (현재 질문 제외)
        previous_messages = state["messages"][:-1]
        chat_history_str = self._format_chat_history(previous_messages)

        # 프롬프트 준비
        prompt = get_stream_prompt()
        prompt_text = prompt.invoke(
            {
                "context": "\n\n".join(
                    [doc.page_content for doc in state["context"]]
                ),
                "chat_history": chat_history_str,
                "question": state["question"],
            }
        )

        return {"prompt_text": prompt_text}

    def _format_chat_history(self, messages: list[BaseMessage]) -> str:
        if not messages:
            return "No previous conversation."

        history_lines = []
        for msg in messages:
            role = "User" if isinstance(msg, HumanMessage) else "Assistant"
            history_lines.append(f"{role}: {msg.content}")

        return "\n".join(history_lines)

    def query(self, text: str) -> QueryResponse:
        """일회성 질의 (히스토리 없음)"""
        result = self.query_graph.invoke({"question": text, "messages": []})

        answer = result["messages"][-1].content
        return QueryResponse(answer=answer)

    def chat(self, text: str, session_id: str) -> Iterator[str]:
        """대화형 질의 (히스토리 포함)"""
        config = {"configurable": {"thread_id": session_id}}
        result = self.chat_graph.invoke(
            {
                "question": text,
                "messages": [HumanMessage(content=text)],
            },
            config=config,
        )

        prompt = result["prompt_text"]

        full_response = ""
        for chunk in self.llm.stream(prompt):
            if chunk.content:
                full_response += chunk.content
                yield chunk.content

        self.chat_graph.update_state(
            config, {"messages": [AIMessage(content=full_response)]}
        )


def get_chain() -> RAGChain:
    return RAGChain()
