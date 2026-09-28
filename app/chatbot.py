import os
from typing import Annotated, List
from typing_extensions import TypedDict
from dotenv import load_dotenv

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from app.vector_db import search_students_in_vector_db

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 1. State holding conversation history and retrieval context
class ChatState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    context: str


# 2. LLM Configuration
llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=api_key,
)


# 3. Retrieve node
def retrieve_node(state: ChatState):
    latest_user_message = state["messages"][-1].content
    results = search_students_in_vector_db(latest_user_message, n_results=2)
    docs = results.get("documents", [[]])[0]
    context = "\n---\n".join(docs) if docs else "No matching student found."
    return {"context": context}


# 4. Generate node incorporating context and chat history
def generate_node(state: ChatState):
    context = state.get("context", "")

    system_instruction = (
        "You are an assistant answering questions about students using the provided database records.\n"
        f"Database Records:\n{context}\n\n"
        "Use the previous chat history to resolve references (like 'he', 'she', or 'that student')."
    )

    full_conversation = [AIMessage(content=system_instruction)] + state[
        "messages"
    ]
    response = llm.invoke(full_conversation)

    if isinstance(response.content, list):
        answer_text = "".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in response.content
        )
    else:
        answer_text = str(response.content)

    return {"messages": [AIMessage(content=answer_text)]}


# 5. Build and compile with in-memory checkpointer
workflow = StateGraph(ChatState)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("generate", generate_node)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

memory = MemorySaver()
student_agent = workflow.compile(checkpointer=memory)