from datetime import datetime
from typing import List, Optional

from core.database import Base
from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Webtoon(Base):
    __tablename__ = "webtoons"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    genre_name: Mapped[str] = mapped_column(String(20), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    subtitle: Mapped[Optional[str]]
    picture_writer: Mapped[Optional[str]] = mapped_column(String(100))
    script_writer: Mapped[Optional[str]] = mapped_column(String(100))
    outline: Mapped[Optional[str]] = mapped_column(Text)
    nation_code: Mapped[str] = mapped_column(String(10), nullable=False)
    publish_platform: Mapped[Optional[str]] = mapped_column(String(50))
    publish_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    images: Mapped[List["WebtoonImage"]] = relationship(
        back_populates="webtoon"
    )


class WebtoonImage(Base):
    __tablename__ = "webtoon_images"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    mastr_id: Mapped[str] = mapped_column(String(20), unique=True)
    url: Mapped[str] = mapped_column(unique=True)
    index: Mapped[int] = mapped_column(unique=True, index=True)

    webtoon_id: Mapped[int] = mapped_column(ForeignKey(Webtoon.id))

    webtoon: Mapped[Webtoon] = relationship(back_populates="images")
