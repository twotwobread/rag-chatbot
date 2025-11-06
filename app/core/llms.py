from langchain_google_genai.chat_models import ChatGoogleGenerativeAI

from app.core.config import settings

llm = ChatGoogleGenerativeAI(
    model=settings.GEMINI_MODEL,
    google_api_key=settings.GOOGLE_API_KEY,
    streaming=True,
)
