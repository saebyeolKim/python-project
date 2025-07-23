from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from dataclasses import dataclass
from dependency_injector.wiring import inject, Provide
from datetime import datetime
from typing import Annotated
from common.auth import CurrnetUser, get_current_user
from note.application.note_service import NoteService
from containers import Container

router = APIRouter(prefix="/note")

class NoteResponse(BaseModel):
    id: str
    user_id: str
    title: str
    content: str
    memo_date: str
    tags: list[str]
    created_at: datetime
    update_at: datetime

class CreateNoteBody(BaseModel):
    title: str = Field(min_length=1, max_length=64)
    content: str = Field(min_length=1)
    memo_date: str = Field(min_length=8, max_length=8)
    tags: list[str] | None = Field(
        default=None, min_length=1, max_length=32,
    )
