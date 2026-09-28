import uuid
import requests
import streamlit as st

st.set_page_config(page_title="Student Database Assistant", page_icon="🎓")

API_URL = "http://127.0.0.1:8000/chat"

# 1. Initialize session state FIRST
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Title & Sidebar Controls
st.title("🎓 Student AI Database Assistant")

with st.sidebar:
    st.markdown("---")
    st.subheader("Database Overview")
    if st.button("📊 View All Students", use_container_width=True):
        try:
            students_res = requests.get(
                "http://127.0.0.1:8000/students", timeout=10
            )
            if students_res.status_code == 200:
                st.dataframe(students_res.json())
            else:
                st.warning("Failed to fetch students.")
        except Exception as e:
            st.error(f"Error: {e}")
    st.subheader("Session Controls")
    if st.button("🔄 New Conversation", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.caption(f"Active Thread: `{st.session_state.session_id[:8]}...`")

# 3. Render previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat input handling
if prompt := st.chat_input("Ask a question about any student..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching records..."):
            try:
                response = requests.post(
                    API_URL,
                    json={
                        "question": prompt,
                        "session_id": st.session_state.session_id,
                    },
                    timeout=30,
                )
                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer found.")
                else:
                    answer = f"⚠️ Server Error ({response.status_code}): {response.text}"
            except Exception as e:
                answer = f"⚠️ Connection error: {e}"

            st.markdown(answer)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )