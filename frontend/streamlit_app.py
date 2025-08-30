
import streamlit as st
import requests


BACKEND_URL = "http://127.0.0.1:8000/chat"


if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.title("HR Chatbot with RAG + Groq")


for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


if prompt := st.chat_input("Ask about employees, skills, projects..."):
    
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    
    try:
        response = requests.post(BACKEND_URL, json={"query": prompt})
        data = response.json()
        answer = data.get("response", "No response from backend")
    except Exception as e:
        answer = f"Error: {e}"

    
    st.session_state["messages"].append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
