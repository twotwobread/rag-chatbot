from langchain_community.document_loaders import Docx2txtLoader

from app.core.config import settings


def get_docx_loader() -> Docx2txtLoader:
    return Docx2txtLoader(
        file_path=f"{settings.ROOT_PATH}/data/copyright-law.docx"
    )
