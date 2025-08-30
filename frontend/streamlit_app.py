
import streamlit as st
import sys
import os
import json
import re
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent / "backend"))

try:
    from rag_engine import RAGEngine
    from groq_client import ask_groq
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()


@st.cache_resource
def load_rag_engine():
    try:
        
        possible_paths = [
            Path(__file__).parent.parent / "backend" / "employees.json",
            Path("backend") / "employees.json",
            Path("employees.json")
        ]
        
        for path in possible_paths:
            if path.exists():
               
                rag = RAGEngine(str(path))
                return rag
        
        st.error("employees.json not found in any expected location")
        return None
        
    except Exception as e:
        st.error(f"Error loading RAG engine: {e}")
        return None


if "messages" not in st.session_state:
    st.session_state["messages"] = []


rag = load_rag_engine()

if rag is None:
    st.error("Failed to load RAG engine. Please check the backend files.")
    st.stop()

st.title("HR Resource Query Chatbot")


for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


if prompt := st.chat_input("Ask about employees, skills, projects..."):
   
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

   
    try:
        q_lower = prompt.lower()
        
       
        if "total" in q_lower and ("employee" in q_lower or "count" in q_lower):
            
            results = rag.employees
            answer = f"There are {len(results)} employees in total.\n\n"
            answer += "All employees:\n"
            for emp in results:
                answer += f"- {emp['name']} ({emp['experience_years']} years, {emp['availability']})\n"
        else:
           
            min_exp = None
            exp_match = re.search(r'(\d+)\s*(\+|or more)?\s*years', q_lower)
            if exp_match:
                min_exp = int(exp_match.group(1))

            
            available_only = False
            if "available" in q_lower:
                available_only = True

            
            if "devops" in q_lower or "kubernetes" in q_lower:
               
                devops_employees = []
                for emp in rag.employees:
                    emp_skills_lower = [s.lower() for s in emp["skills"]]
                    if any(skill in emp_skills_lower for skill in ["docker", "terraform", "aws", "kubernetes"]):
                        if not available_only or emp["availability"].lower() == "available":
                            devops_employees.append(emp)
                results = devops_employees
            else:
                
                results = rag.search(
                    prompt, 
                    min_experience=min_exp, 
                    available_only=available_only
                )

            if not results:
                answer = f"Sorry, no employees match '{prompt}'."
            else:
               
                context = "\n".join([
                    f"{emp['name']} has {emp['experience_years']} years of experience in {', '.join(emp['skills'])}. "
                    f"Projects: {', '.join(emp['projects'])}. Availability: {emp['availability']}."
                    for emp in results
                ])

                
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

   
    st.session_state["messages"].append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
