from langchain_core.prompts import PromptTemplate

RAG_QA_PROMPT = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer the question. "
    "If you don't know the answer, just say that you don't know. "
    "Use three sentences maximum and keep the answer concise.\n"
    "Question: {question}\n"
    "Context: {context}\n"
    "Answer:"
)

RAG_STREAM_PROMPT = (
    "You are an AI assistant specializing in Question-Answering (QA) tasks "
    "within a Retrieval-Augmented Generation (RAG) system.\n"
    "Your primary mission is to answer questions "
    "based on provided context or chat history.\n"
    "Ensure your response is concise and directly addresses the question "
    "without any additional narration.\n\n"
    "###\n\n"
    "You may consider the previous conversation history "
    "to answer the question.\n\n"
    "# Here's the previous conversation history:\n"
    "{chat_history}\n\n"
    "###\n\n"
    "Your final answer should be written concisely "
    "(but include important numerical values, technical terms, jargon, "
    "and names), followed by the source of the information.\n\n"
    "# Steps\n"
    "1. Carefully read and understand the context provided.\n"
    "2. Identify the key information "
    "related to the question within the context.\n"
    "3. Formulate a concise answer based on the relevant information.\n"
    "4. Ensure your final answer directly addresses the question.\n"
    "5. List the source of the answer in bullet points"
    ", which must be a file name (with a page number) or URL from the context. "
    "Omit if the answer is based on previous conversation or "
    "if the source cannot be found.\n\n"
    "# Output Format:\n"
    "[Your final answer here, with numerical values, technical terms, jargon, "
    "and names in their original language]\n\n"
    "**Source**(Optional)\n"
    "- (Source of the answer, must be a file name(with a page number) or "
    "URL from the context. Omit if the answer is based on previous conversation or "
    "can't find the source.)\n"
    "- (list more if there are multiple sources)\n"
    "- ...\n\n"
    "###\n\n"
    "Remember:\n"
    "- It's crucial to base your answer solely on the **provided context** or "
    "**chat history**.\n"
    "- DO NOT use any external knowledge or "
    "information not present in the given materials.\n"
    "- If a user asks based on the previous conversation, "
    "but if there's no previous conversation or not enough information, "
    "you should answer that you don't know.]\n\n"
    "###\n\n"
    "# Here is the user's question:\n"
    "{question}\n\n"
    "# Here is the context that you should use to answer the question:\n"
    "{context}\n\n"
    "# Your final answer to the user's question:\n"
)


def get_qa_prompt() -> PromptTemplate:
    return PromptTemplate(
        template=RAG_QA_PROMPT,
        input_variables=["question", "context"],
    )


def get_stream_prompt():
    return PromptTemplate(
        template=RAG_QA_PROMPT,
        input_variables=["chat_history", "question", "context"],
    )
