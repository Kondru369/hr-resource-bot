
import streamlit as st
import sys
import os
import json
import re
from pathlib import Path

# Add backend to path for imports
sys.path.append(str(Path(__file__).parent.parent / "backend"))

try:
    from rag_engine import RAGEngine
    from groq_client import ask_groq
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Initialize RAG engine
@st.cache_resource
def load_rag_engine():
    try:
        # Try to load from backend directory
        backend_path = Path(__file__).parent.parent / "backend" / "employees.json"
        if backend_path.exists():
            return RAGEngine(str(backend_path))
        else:
            st.error("employees.json not found in backend directory")
            return None
    except Exception as e:
        st.error(f"Error loading RAG engine: {e}")
        return None

# Initialize the app
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Load RAG engine
rag = load_rag_engine()

if rag is None:
    st.error("Failed to load RAG engine. Please check the backend files.")
    st.stop()

st.title("HR Resource Query Chatbot")

# Display chat messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask about employees, skills, projects..."):
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process query
    try:
        # Parse query for experience and skills
        q_lower = prompt.lower()
        
        # Extract experience requirement
        min_exp = None
        exp_match = re.search(r'(\d+)\s*(\+|or more)?\s*years', q_lower)
        if exp_match:
            min_exp = int(exp_match.group(1))

        # Determine skill category
        skill_category = None
        if "mobile app" in q_lower or "ios" in q_lower or "flutter" in q_lower or "react native" in q_lower:
            skill_category = "mobile app"
        elif "backend" in q_lower:
            skill_category = "backend"
        elif "ui/ux" in q_lower or "designer" in q_lower or "figma" in q_lower:
            skill_category = "ui/ux"
        elif "devops" in q_lower or "docker" in q_lower or "terraform" in q_lower or "aws" in q_lower:
            skill_category = "devops"

        # Check for availability filter
        available_only = False
        if "devops" in q_lower or "kubernetes" in q_lower:
            available_only = True
        elif "available" in q_lower:
            available_only = True

        # Search for employees
        results = rag.search(
            prompt, 
            min_experience=min_exp, 
            skill_category=skill_category, 
            available_only=available_only
        )

        if not results:
            answer = f"Sorry, no employees match '{prompt}'."
        else:
            # Create context for LLM
            context = "\n".join([
                f"{emp['name']} has {emp['experience_years']} years of experience in {', '.join(emp['skills'])}. "
                f"Projects: {', '.join(emp['projects'])}. Availability: {emp['availability']}."
                for emp in results
            ])

            # Generate response using LLM
            llm_prompt = f"""
You are an HR assistant. Use ONLY the employees listed in the context below.
Answer naturally and summarize if multiple employees match.
You may categorize by skills or availability.
Do NOT invent skills or experience beyond what is explicitly listed.

Context:
{context}

Question: {prompt}
"""

            answer = ask_groq(llm_prompt)

    except Exception as e:
        answer = f"Error processing query: {str(e)}"

    # Add assistant response
    st.session_state["messages"].append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
