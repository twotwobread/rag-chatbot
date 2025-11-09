from dataclasses import dataclass
from datetime import datetime
from urllib.parse import quote_plus

from sqlalchemy import Column, DateTime, inspect, text
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped
from utils import now_utc


class Base(AsyncAttrs, DeclarativeBase):
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), index=True, default=now_utc
    )
    updated_at: Mapped[datetime] = Column(
        DateTime(timezone=True), default=now_utc, onupdate=now_utc
    )


@dataclass
class DBConfig:
    mode: str
    host: str
    port: int
    schema: str
    user: str
    password: str
    scheme: str


def create_db_uri(config: DBConfig) -> str:
    if config.mode == "sqlite":
        return f"{config.scheme}:///{config.host}"

    return (
        f"{config.scheme}://{config.user}:{quote_plus(config.password)}"
        f"@{config.host}:{config.port}/{config.schema}"
    )


class AsyncDatabaseManager:
    def __init__(self, config: DBConfig):
        self.config = config

        database_uri = create_db_uri(config)
        self.engine = create_async_engine(
            database_uri, pool_size=20, pool_pre_ping=True
        )
        Base.metadata.create_all(self.engine)
        print(f"Database created '{config.mode}' at {config.host}")

        self.inspector = inspect(self.engine.sync_engine)
        self.session_factory = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )

    async def execute_query(self, query: str) -> list[dict]:
        async with self.session_factory() as session:
            result = await session.execute(text(query))
            return [dict(row._mapping) for row in result]

    async def get_format_schema(self) -> str:
        """LLM용 스키마 포맷"""
        tables = await self.get_all_tables()
        schema_parts = []

        for table in tables:
            columns = await self.get_table_columns(table)
            col_descriptions = [
                f"  - {col['column_name']} ({col['data_type']})"
                for col in columns
            ]
            schema_parts.append(
                f"Table: {table}\n" + "\n".join(col_descriptions)
            )

        return "\n\n".join(schema_parts)

    async def get_all_tables(self) -> list[str]:
        """모든 테이블 목록"""
        query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """
        results = await self.execute_query(query)
        return [row["table_name"] for row in results]

    async def get_table_columns(self, table_name: str) -> list[dict]:
        """테이블 컬럼 정보"""
        query = """
            SELECT 
                column_name,
                data_type,
                is_nullable,
                column_default,
                character_maximum_length
            FROM information_schema.columns
            WHERE table_schema = 'public' 
            AND table_name = :table_name
            ORDER BY ordinal_position
        """
        return await self.execute_query(query, {"table_name": table_name})

    def get_format_relations(self) -> str:
        """프롬프트용 포맷으로 변환"""
        relationships = self.get_all_relationships()

        lines = []
        for table, rels in sorted(relationships.items()):
            if rels:
                lines.append(f"\nTable: {table}")
                for rel in rels:
                    lines.append(
                        f"  - {rel['type']}: {rel['target_table']} "
                        f"via {rel['foreign_key']} -> {rel['target_key']}"
                    )

        return "\n".join(lines)

    def get_all_relationships(self) -> dict[str, list[dict]]:
        """모든 테이블의 관계 맵 생성"""
        table_names = self.inspector.get_table_names(schema="public")

        relationship_map = {}
        fk_reverse_map = {}  # 역방향 관계 추적

        for table_name in table_names:
            relationship_map[table_name] = []

            # Foreign Keys
            fks = self.inspector.get_foreign_keys(table_name)

            for fk in fks:
                # belongs_to 관계
                relationship_map[table_name].append(
                    {
                        "type": "belongs_to",
                        "target_table": fk["referred_table"],
                        "foreign_key": fk["constrained_columns"][0],
                        "target_key": fk["referred_columns"][0],
                        "constraint_name": fk["name"],
                    }
                )

                # 역방향 관계를 위한 정보 저장
                referred_table = fk["referred_table"]
                if referred_table not in fk_reverse_map:
                    fk_reverse_map[referred_table] = []

                fk_reverse_map[referred_table].append(
                    {
                        "type": "has_many",
                        "target_table": table_name,
                        "foreign_key": fk["constrained_columns"][0],
                        "target_key": fk["referred_columns"][0],
                    }
                )

        # 역방향 관계 추가
        for table, reverse_rels in fk_reverse_map.items():
            if table not in relationship_map:
                relationship_map[table] = []
            relationship_map[table].extend(reverse_rels)

        return relationship_map
