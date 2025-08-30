
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
        # Try multiple possible paths
        possible_paths = [
            Path(__file__).parent.parent / "backend" / "employees.json",
            Path("backend") / "employees.json",
            Path("employees.json")
        ]
        
        for path in possible_paths:
            if path.exists():
                # Create RAG engine
                rag = RAGEngine(str(path))
                return rag
        
        st.error("employees.json not found in any expected location")
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
        q_lower = prompt.lower()
        
        # Special handling for total count queries
        if "total" in q_lower and ("employee" in q_lower or "count" in q_lower):
            # Return all employees for total count
            results = rag.employees
            answer = f"There are {len(results)} employees in total.\n\n"
            answer += "All employees:\n"
            for emp in results:
                answer += f"- {emp['name']} ({emp['experience_years']} years, {emp['availability']})\n"
        else:
            # Parse query for experience and skills
            min_exp = None
            exp_match = re.search(r'(\d+)\s*(\+|or more)?\s*years', q_lower)
            if exp_match:
                min_exp = int(exp_match.group(1))

            # Check for availability filter
            available_only = False
            if "available" in q_lower:
                available_only = True

            # Search for employees using simplified approach
            results = rag.search(
                prompt, 
                min_experience=min_exp, 
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
