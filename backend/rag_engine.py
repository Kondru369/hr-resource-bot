import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class RAGEngine:
    def __init__(self, data_path="employees.json"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        with open(data_path, "r") as f:
            self.employees = json.load(f)
        self.index, self.texts = self._build_index()

    def _build_index(self):
        texts = [
            f"{emp['name']} has {emp['experience_years']} years of experience in {', '.join(emp['skills'])}. "
            f"Projects: {', '.join(emp['projects'])}. Availability: {emp['availability']}."
            for emp in self.employees
        ]
        vectors = self.model.encode(texts)
        index = faiss.IndexFlatL2(vectors.shape[1])
        index.add(np.array(vectors, dtype="float32"))
        return index, texts

    def search(self, query, k=10, min_experience=None, available_only=False):
        """
        query: free text query
        k: top candidates from FAISS
        min_experience: optional integer to filter by experience
        available_only: if True, return only available employees
        """
        query_lower = query.lower()
        
        
        if min_experience is not None:
            results = [emp for emp in self.employees if emp["experience_years"] >= min_experience]
            
            results.sort(key=lambda x: x["experience_years"], reverse=True)
        else:
            
            query_vec = self.model.encode([query])
            scores, indices = self.index.search(np.array(query_vec, dtype="float32"), k)
            candidates = [self.employees[i] for i in indices[0]]
            
            
            exact_matches = []
            for emp in self.employees:
                emp_skills = [s.lower() for s in emp["skills"]]
                if any(skill in query_lower for skill in emp_skills):
                    exact_matches.append(emp)
            
            
            all_candidates = exact_matches + candidates
            seen_ids = set()
            results = []
            for emp in all_candidates:
                if emp["id"] not in seen_ids:
                    results.append(emp)
                    seen_ids.add(emp["id"])
        
       
        if available_only:
            results = [emp for emp in results if emp["availability"].lower() == "available"]
        
        return results
