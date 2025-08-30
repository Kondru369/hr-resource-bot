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

    def search(self, query, k=5, min_experience=None, skill_category=None, available_only=False):
        """
        query: free text query
        k: top candidates from FAISS
        min_experience: optional integer to filter by experience
        skill_category: optional string to filter employees by category (e.g., 'mobile app', 'backend')
        available_only: if True, return only available employees
        """
        
        query_vec = self.model.encode([query])
        scores, indices = self.index.search(np.array(query_vec, dtype="float32"), k)
        candidates = [self.employees[i] for i in indices[0]]

        
        query_lower = query.lower()
        boosted = []
        normal = []
        for emp in candidates:
            emp_skills = [s.lower() for s in emp["skills"]]
            matched_exact = any(skill in query_lower for skill in emp_skills)
            if matched_exact:
                boosted.append(emp)
            else:
                normal.append(emp)
        results = boosted + normal

        
        if min_experience is not None:
            results = [emp for emp in self.employees if emp["experience_years"] >= min_experience]

        
        if skill_category:
            skill_category = skill_category.lower()
            mapping = {
                "mobile app": ["react native", "flutter", "swift", "ios development", "dart"],
                "backend": ["java", "spring", "golang", "python", "django", "kubernetes"],
                "ui/ux": ["ui/ux design", "figma", "adobe xd"],
                "devops": ["docker", "terraform", "aws", "kubernetes"]
            }
            category_skills = mapping.get(skill_category, [])
            filtered = []
            for emp in self.employees:  # ← use all employees instead of just FAISS results
                emp_skills_lower = [s.lower() for s in emp["skills"]]
                if any(skill in emp_skills_lower for skill in category_skills):
                    if not available_only or emp["availability"].lower() == "available":
                        filtered.append(emp)
            results = filtered


        
        if available_only:
            results = [emp for emp in results if emp["availability"].lower() == "available"]

        return results
