from functools import lru_cache

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.embeddings import embedding
from app.rag.loaders import get_docx_loader

db = None


def init_vectorstore():
    global db

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
    )

    docx_loader = get_docx_loader()
    document_list = docx_loader.load_and_split(text_splitter)

    db = Chroma.from_documents(
        documents=document_list,
        embedding=embedding,
        collection_name="copyright",
        persist_directory="./chroma",
    )


@lru_cache(maxsize=1)
def get_retriever():
    return db.as_retriever()
