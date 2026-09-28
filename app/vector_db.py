import chromadb

# Initialize ChromaDB client persisted locally in chroma_storage folder
client = chromadb.PersistentClient(path="./chroma_storage")
collection = client.get_or_create_collection(name="students_collection")

def add_student_to_vector_db(student_id: int, student_text: str, metadata: dict):
    collection.upsert(
        ids=[str(student_id)],
        documents=[student_text],
        metadatas=[metadata]
    )

def search_students_in_vector_db(query: str, n_results: int = 2):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results