from sqlalchemy.orm import Session
from app.models import Student
from app.schemas import StudentCreate, StudentUpdate
from app.vector_db import add_student_to_vector_db, collection


def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Student).offset(skip).limit(limit).all()


def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()


def create_student(db: Session, student: StudentCreate):
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    # Sync into ChromaDB
    try:
        add_student_to_vector_db(db_student)
    except Exception as e:
        print(f"ChromaDB insert failed: {e}")

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
    try:
        add_student_to_vector_db(db_student)
    except Exception as e:
        print(f"ChromaDB update failed: {e}")

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