from fastapi import FastAPI, Query
from pydantic import BaseModel
from rag_engine import RAGEngine
from groq_client import ask_groq
import re

app = FastAPI()
rag = RAGEngine("employees.json")

class ChatRequest(BaseModel):
    query: str


@app.get("/employees/search")
def search_employees(query: str = Query(..., description="Search for skills or experience")):
    q_lower = query.lower()
    min_exp = None
    exp_match = re.search(r'(\d+)\s*(\+|or more)?\s*years', q_lower)
    if exp_match:
        min_exp = int(exp_match.group(1))

    available_only = "available" in q_lower or "devops" in q_lower or "kubernetes" in q_lower

   
    if ("total" in q_lower and ("employee" in q_lower or "count" in q_lower)) \
       or ("list" in q_lower and "name" in q_lower):
        return {
            "response": f"There are {len(rag.employees)} employees in total.\n\n" +
                        "All employee names: " + " ".join(emp["name"] for emp in rag.employees),
            "employees": rag.employees
        }

    
    elif "devops" in q_lower or "docker" in q_lower or "terraform" in q_lower or "aws" in q_lower or "kubernetes" in q_lower:
        results = []
        for emp in rag.employees:
            emp_skills_lower = [s.lower() for s in emp["skills"]]
            if any(skill in emp_skills_lower for skill in ["docker", "terraform", "aws", "kubernetes"]):
                if not available_only or emp["availability"].lower() == "available":
                    results.append(emp)
    else:
     
        results = rag.search(query, min_experience=min_exp, available_only=available_only)

    if not results:
        return {"response": f"Sorry, no employees match '{query}'.", "employees": []}

    response_lines = []
    for emp in results:
        availability = "available" if emp["availability"].lower() == "available" else "unavailable"
        response_lines.append(
            f"{emp['name']} has {emp['experience_years']} years of experience in {', '.join(emp['skills'])}. "
            f"Projects: {', '.join(emp['projects'])}. Currently {availability}."
        )

    return {"response": "\n".join(response_lines), "employees": results}


@app.post("/chat")
def chat(request: ChatRequest):
    q_lower = request.query.lower()
    min_exp = None
    exp_match = re.search(r'(\d+)\s*(\+|or more)?\s*years', q_lower)
    if exp_match:
        min_exp = int(exp_match.group(1))

    available_only = "available" in q_lower or "devops" in q_lower or "kubernetes" in q_lower

    
    if ("total" in q_lower and ("employee" in q_lower or "count" in q_lower)) \
       or ("list" in q_lower and "name" in q_lower):
        return {
            "response": f"There are {len(rag.employees)} employees in total.\n\n" +
                        "All employee names: " + " ".join(emp["name"] for emp in rag.employees),
            "context": "\n".join(
                f"{emp['name']} has {emp['experience_years']} years of experience in {', '.join(emp['skills'])}. "
                f"Projects: {', '.join(emp['projects'])}. Availability: {emp['availability']}."
                for emp in rag.employees
            ),
            "employees": rag.employees
        }

   
    elif "devops" in q_lower or "docker" in q_lower or "terraform" in q_lower or "aws" in q_lower or "kubernetes" in q_lower:
        results = []
        for emp in rag.employees:
            emp_skills_lower = [s.lower() for s in emp["skills"]]
            if any(skill in emp_skills_lower for skill in ["docker", "terraform", "aws", "kubernetes"]):
                if not available_only or emp["availability"].lower() == "available":
                    results.append(emp)
    else:
      
        results = rag.search(request.query, min_experience=min_exp, available_only=available_only)

    if not results:
        return {"response": f"Sorry, no employees match '{request.query}'.", "context": "", "employees": []}

    context = "\n".join([
        f"{emp['name']} has {emp['experience_years']} years of experience in {', '.join(emp['skills'])}. "
        f"Projects: {', '.join(emp['projects'])}. Availability: {emp['availability']}."
        for emp in results
    ])

    prompt = f"""
You are an HR assistant. Use ONLY the employees listed in the context below.
Answer naturally and summarize if multiple employees match.
You may categorize by skills or availability.
Do NOT invent skills or experience beyond what is explicitly listed.

Context:
{context}

Question: {request.query}
"""

    answer = ask_groq(prompt)
    return {"response": answer, "context": context, "employees": results}
