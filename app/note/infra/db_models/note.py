from database import Base
from datetime import datetime
from sqlalchemy import String, DateTime, Text, Table, Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

note_tag_association = Table(
    "Note_Tag",
    Base.metadata,
    Column("note_id", String(36), ForeignKey("Note.id")),
    Column("tag_id", String(36), ForeignKey("Tag.id")),
)

class Note(Base):
    __tablename__ = "Note"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), nullable=False)
    title = Column(String(64), nullable=False)
    content = Column(Text, nullable=False)
    memo_date = Column(String(8), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

    tags = relationship(
        "Tag",
        secondary=note_tag_association,
        back_populates="notes",
        lazy="joined",
    )

class Tag(Base):
    __tablename__ = "Tag"

    id = Column(String(36), primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

    notes = relationship(
        "Note",
        secondary=note_tag_association,
        back_populates="tags",
        lazy="joined",
    )