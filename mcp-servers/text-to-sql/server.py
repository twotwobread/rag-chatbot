from core.config import settings
from core.database import AsyncDatabaseManager, DBConfig
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from mcp.server.fastmcp import FastMCP
from mcp.types import Tool
from prompts import create_advanced_text_to_sql_prompt

llm = ChatGoogleGenerativeAI(
    model=settings.GEMINI_MODEL,
    google_api_key=settings.GOOGLE_API_KEY,
    streaming=True,
)

mcp = FastMCP("Text-to-SQL")


@mcp.tool()
async def query_database(question: str) -> int:
    db_config = DBConfig(
        mode=settings.DB_MODE,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        schema=settings.DB_SCHEMA,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        scheme=settings.DB_SCHEME,
    )
    db_manager = AsyncDatabaseManager(config=db_config)

    format_schema = await db_manager.get_format_schema()
    format_relation = db_manager.get_format_relations()

    prompt = create_advanced_text_to_sql_prompt(
        question,
        format_schema,
        format_relation,
    )
    response = llm.invoke(prompt)
    sql_query = response.content

    return await db_manager.execute_query(sql_query)


@mcp.list_tools()
def get_list_tools():
    return [
        Tool(
            name="query_database",
            description="자연어 질문을 SQL로 변환하여 데이터베이스에 쿼리한 응답을 반환합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "데이터베이스에 관련된 자연어 질문",
                    }
                },
                "required": ["question"],
            },
        )
    ]


if __name__ == "__main__":
    mcp.run(transport="stdio")
