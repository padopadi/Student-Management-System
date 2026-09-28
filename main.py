from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.vector_db import add_student_to_vector_db
from app.schemas import StudentCreate, StudentUpdate, ChatRequest, ChatResponse
from app.chatbot import student_agent
from app.database import Base, engine, SessionLocal
from app.models import Student
from app.schemas import StudentCreate, StudentUpdate
from langchain_core.messages import HumanMessage
from app.crud import create_student, get_students, get_student, update_student, delete_student
Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Student AI Backend is working!"}


@app.post("/students")
def add_student(student_data: StudentCreate, db: Session = Depends(get_db)):
    student = create_student(db, student_data)
    
    # Also index this student in ChromaDB for AI semantic search!
    student_summary = (
        f"Student Name: {student.name}, Course: {student.course}, "
        f"Year: {student.year}, CGPA: {student.cgpa}, Skills: {student.skills}"
    )
    add_student_to_vector_db(
        student_id=student.id,
        student_text=student_summary,
        metadata={"name": student.name, "email": student.email}
    )
    
    return student
@app.get("/students")
def get_all_students(
    db: Session = Depends(get_db)
):

    students = get_students(db)

    return students
@app.get("/students/{student_id}")
def get_one_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = get_student(db, student_id)

    return student
@app.put("/students/{student_id}")
def update_one_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db)
):

    student = update_student(db, student_id, student_data)

    return student
@app.delete("/students/{student_id}")
def remove_student(student_id: int, db: Session = Depends(get_db)):
    student = delete_student(db, student_id)

    if student is None:
        return {"message": "Student not found"}

    return {"message": "Student deleted successfully"}
@app.post("/chat", response_model=ChatResponse)
def chat_with_students(request: ChatRequest):
    try:
        config = {
            "configurable": {
                "thread_id": request.session_id or "default_user"
            }
        }
        result = student_agent.invoke(
            {"messages": [HumanMessage(content=request.question)]},
            config=config,
        )
        last_message = result["messages"][-1]
        return {"answer": last_message.content}
    except Exception as e:
        print(f"\n---> CHATBOT ERROR: {repr(e)}\n")
        raise HTTPException(status_code=500, detail=str(e))