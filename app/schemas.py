from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    email: str
    course: str
    year: int
    cgpa: float
    skills: str
class StudentUpdate(BaseModel):
    name: str
    email: str
    course: str
    year: int
    cgpa: float
    skills: str
class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = "default_user"


class ChatResponse(BaseModel):
    answer: str  
