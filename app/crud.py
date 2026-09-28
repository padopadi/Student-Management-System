from sqlalchemy.orm import Session
from app.models import Student
from app.schemas import StudentCreate, StudentUpdate
from app.vector_db import add_student_to_vector_db, collection


def create_student(db: Session, student: StudentCreate):
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    # Sync into ChromaDB vector database
    add_student_to_vector_db(db_student)
    return db_student


def update_student(db: Session, student_id: int, student_update: StudentUpdate):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        return None

    for key, value in student_update.model_dump(exclude_unset=True).items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)

    # Upsert updated record into ChromaDB
    add_student_to_vector_db(db_student)
    return db_student


def delete_student(db: Session, student_id: int):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        return None

    db.delete(db_student)
    db.commit()

    # Remove student vector from ChromaDB
    try:
        collection.delete(ids=[str(student_id)])
    except Exception as e:
        print(f"ChromaDB deletion skipped: {e}")

    return db_student