# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Setup Environment
```bash
# Clone and setup
git clone <your-repo-url>
cd hr-resource-bot
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Add Your API Key
Create `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Start Services
**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
streamlit run streamlit_app.py
```

### 4. Test the Chatbot
Open http://localhost:8501 and try these queries:

- "Who are the most experienced employees (7+ years)?"
- "Find React Native developers"
- "Who can work on a DevOps project?"
- "Show me Machine Learning specialists"
- "Find available Python developers"

## 🧪 Test Queries

The chatbot handles various query types:

### Experience-based
- "Find employees with 5+ years experience"
- "Who are the most experienced employees?"

### Skill-based
- "Find Python developers"
- "Show me Machine Learning specialists"
- "Who knows React Native?"

### Availability-based
- "Find available DevOps engineers"
- "Who is available for mobile app development?"

### Project-based
- "Who has worked on healthcare projects?"
- "Find people with e-commerce experience"

## 📊 Sample Responses

The system provides:
- Employee names and experience years
- Key skills and relevant projects
- Availability status (✅ available / ❌ busy)
- Natural language explanations

## 🔧 Troubleshooting

**Backend won't start:**
- Check if port 8000 is free
- Ensure all dependencies are installed
- Verify `.env` file has GROQ_API_KEY

**Frontend won't connect:**
- Make sure backend is running on http://127.0.0.1:8000
- Check if port 8501 is available

**No responses:**
- Verify your Groq API key is valid
- Check internet connection for API calls
