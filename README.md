# 🎓 AI-Augmented Student Management System

An intelligent, full-stack Student Management System combining traditional relational CRUD operations with agentic semantic search and multi-turn conversational memory.

## 🚀 Live Demo
- **Frontend App**: [Streamlit Cloud UI](https://student-management-system-32bktyc3nmg8tjxnwjdpds.streamlit.app)
- **API Documentation**: [FastAPI Swagger UI](https://student-management-api.onrender.com/docs)
- - **Interactive API Docs**: [https://student-management-api-mdwd.onrender.com/docs](https://student-management-api-mdwd.onrender.com/docs#/default/add_student_students_post)

---

## 🛠️ Architecture & Tech Stack

- **Backend**: FastAPI (Python 3.12+), Pydantic v2, Uvicorn
- **Relational Storage**: SQLite with SQLAlchemy ORM (Full CRUD operations)
- **Vector Database**: ChromaDB (Automated vector synchronization on DB insert/update/delete)
- **AI Agent & Memory**: LangGraph state graph with `MemorySaver` checkpointing for multi-turn session persistence
- **LLM**: Google Gemini
- **Frontend**: Streamlit
- **Deployment**: Render (Backend Web Service) + Streamlit Community Cloud (Frontend)

---

## ✨ Features

- **Full RESTful CRUD**: Endpoints for creating, retrieving, updating, and deleting student records.
- **Semantic Vector Search**: Natural language query retrieval based on student skills, courses, and bios.
- **Multi-Turn Chat History**: Retains context across questions (e.g., resolving pronouns like "What is his CGPA?" after identifying a student).
- **Live Database Inspection**: In-app tabular view of the underlying student database.

---

## 💻 Local Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/padopadi/Student-Management-System.git](https://github.com/padopadi/Student-Management-System.git)
   cd Student-Management-System
