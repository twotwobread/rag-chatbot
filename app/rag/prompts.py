from langchain_core.prompts import PromptTemplate

RAG_PROMPT = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer the question. "
    "If you don't know the answer, just say that you don't know. "
    "Use three sentences maximum and keep the answer concise.\n"
    "Question: {question}\n"
    "Context: {context}\n"
    "Answer:"
)


def get_rag_prompt() -> PromptTemplate:
    return PromptTemplate(
        template=RAG_PROMPT,
        input_variables=["question", "context"],
    )
