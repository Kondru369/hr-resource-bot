
from fastapi import FastAPI, Query
from pydantic import BaseModel
from rag_engine import RAGEngine
from groq_client import ask_groq

app = FastAPI()


rag = RAGEngine("employees.json")


class ChatRequest(BaseModel):
    query: str


@app.get("/employees/search")
def search_employees(query: str = Query(..., description="Search for skills or experience")):
    employees = rag.search(query)

    if not employees:
        return {
            "response": f"No employees found for '{query}'.",
            "employees": []
        }

  
    response_lines = []
    for emp in employees:
        availability = "available ✅" if emp["availability"].lower() == "available" else "unavailable ❌"
        response_lines.append(
            f"{emp['name']} has {emp['experience_years']} years of experience in {', '.join(emp['skills'])}. "
            f"They worked on {', '.join(emp['projects'])}. Currently {availability}."
        )

    response_text = "\n".join(response_lines)

    return {
        "response": response_text,
        "employees": employees 
    }


@app.post("/chat")
def chat(request: ChatRequest):
    import re
    q_lower = request.query.lower()


    min_exp = None
    exp_match = re.search(r'(\d+)\s*(\+|or more)?\s*years', q_lower)
    if exp_match:
        min_exp = int(exp_match.group(1))


    skill_category = None
    if "mobile app" in q_lower or "ios" in q_lower or "flutter" in q_lower or "react native" in q_lower:
        skill_category = "mobile app"
    elif "backend" in q_lower:
        skill_category = "backend"
    elif "ui/ux" in q_lower or "designer" in q_lower or "figma" in q_lower:
        skill_category = "ui/ux"
    elif "devops" in q_lower or "docker" in q_lower or "terraform" in q_lower or "aws" in q_lower:
        skill_category = "devops"

  
    available_only = False

   
    if "devops" in q_lower or "kubernetes" in q_lower:
        available_only = True
    elif "available" in q_lower:
        available_only = True


   
    results = rag.search(
        request.query, 
        min_experience=min_exp, 
        skill_category=skill_category, 
        available_only=available_only
    )

    if not results:
        return {"response": f"Sorry, no employees match '{request.query}'.", "context": ""}

    
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
    return {"response": answer, "context": context}
