from sqlalchemy import Column, Integer, String, Float

from app.database import Base


class Student(Base):

    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    email = Column(String, unique=True)

    course = Column(String)

    year = Column(Integer)

    cgpa = Column(Float)

    skills = Column(String)