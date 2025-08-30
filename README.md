# HR Resource Query Chatbot

## Overview
An intelligent HR assistant chatbot that helps HR teams find employees by answering natural language queries about skills, experience, and project requirements. The system uses a RAG (Retrieval-Augmented Generation) approach with semantic search and AI-powered responses to provide relevant employee recommendations.

## Features
- **Natural Language Queries**: Ask questions like "Find Python developers with 3+ years experience" or "Who has worked on healthcare projects?"
- **Semantic Search**: Uses sentence transformers and FAISS for intelligent employee matching
- **AI-Powered Responses**: Integrates with Groq LLM for natural language generation
- **Smart Filtering**: Filter by experience level, skill categories, and availability
- **Real-time Chat Interface**: Streamlit-based chat interface for easy interaction
- **RESTful API**: FastAPI backend with automatic documentation

## Architecture

### System Components
1. **Frontend**: Streamlit chat interface for user interaction
2. **Backend API**: FastAPI server handling chat requests and employee search
3. **RAG Engine**: Semantic search using sentence transformers and FAISS
4. **LLM Integration**: Groq API for natural language response generation
5. **Data Layer**: JSON-based employee database with 15+ sample employees

### RAG Pipeline
1. **Retrieval**: FAISS vector search using sentence embeddings
2. **Augmentation**: Combine retrieved employee data with query context
3. **Generation**: LLM generates natural language responses with recommendations

### Technology Stack
- **Backend**: FastAPI, Python 3.11+
- **Frontend**: Streamlit
- **AI/ML**: Sentence Transformers, FAISS, Groq LLM
- **Data**: JSON files with structured employee information
- **Deployment**: Local development setup with virtual environment

## Setup & Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd hr-resource-bot
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Start the backend server**
   ```bash
   python run_backend.py
   ```

6. **Start the frontend (in a new terminal)**
   ```bash
   python run_frontend.py
   ```

7. **Access the application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## API Documentation

### Endpoints

#### POST /chat
Process natural language queries and return AI-generated responses.

**Request Body:**
```json
{
  "query": "Find Python developers with 3+ years experience"
}
```

**Response:**
```json
{
  "response": "Based on your requirements, I found several Python developers...",
  "context": "Employee details and context..."
}
```

#### GET /employees/search
Search employees by skills or experience.

**Query Parameters:**
- `query` (string): Search term for skills or experience

**Response:**
```json
{
  "response": "Formatted employee information...",
  "employees": [
    {
      "id": 1,
      "name": "Alice Johnson",
      "skills": ["Python", "React", "AWS"],
      "experience_years": 5,
      "projects": ["E-commerce Platform", "Healthcare Dashboard"],
      "availability": "available"
    }
  ]
}
```

### Sample Queries
- "Find developers who know both AWS and Docker"
- "Who has worked on healthcare projects?"
- "Suggest people for a React Native project"
- "Find Python developers with 5+ years experience"
- "Show available DevOps engineers"

## AI Development Process

### AI Tools Used
- **Cursor AI**: Primary coding assistant for code generation and architecture decisions
- **GitHub Copilot**: Assisted with boilerplate code and API patterns
- **ChatGPT**: Helped with debugging and optimization strategies

### AI Assistance Breakdown
- **Code Generation**: ~60% - AI helped generate the RAG engine, API endpoints, and frontend components
- **Architecture Decisions**: ~25% - AI assisted with technology choices and system design
- **Debugging**: ~10% - AI helped troubleshoot integration issues
- **Manual Implementation**: ~5% - Custom business logic and specific filtering requirements

### AI-Generated Solutions
- **RAG Pipeline**: AI suggested the sentence transformers + FAISS approach for semantic search
- **API Structure**: AI recommended FastAPI for automatic documentation and async support
- **Frontend Design**: AI helped design the Streamlit chat interface with proper state management

### Challenges Where AI Couldn't Help
- **Business Logic**: Specific filtering requirements for skill categories and availability
- **Data Structure**: Custom employee data format and project categorization
- **Integration Issues**: Specific error handling for API failures and edge cases

## Technical Decisions

### Technology Choices

#### OpenAI vs Open Source
- **Chosen**: Groq API for its speed and cost-effectiveness
- **Reasoning**: Faster response times compared to OpenAI, good balance of cost and performance

#### Local vs Cloud LLM
- **Chosen**: Cloud-based Groq API
- **Trade-offs**: 
  - Pros: No setup complexity, consistent performance, cost-effective
  - Cons: Requires internet connection, API dependency

#### Performance vs Cost vs Privacy
- **Performance**: FAISS for fast vector search, sentence transformers for quality embeddings
- **Cost**: Groq API provides good performance at reasonable cost
- **Privacy**: Local embedding generation, only queries sent to cloud LLM

### Architecture Trade-offs
- **JSON vs Database**: Chose JSON for simplicity and quick development
- **Streamlit vs React**: Streamlit for rapid prototyping and Python-native development
- **FAISS vs Elasticsearch**: FAISS for lightweight, in-memory vector search

## Future Improvements

### Short-term (1-2 weeks)
- Add authentication and user management
- Implement employee availability scheduling
- Add project timeline and resource allocation features
- Enhance error handling and validation

### Medium-term (1-2 months)
- Migrate to PostgreSQL with vector extensions
- Add employee skill assessment and certification tracking
- Implement team formation recommendations
- Add analytics dashboard for resource utilization

### Long-term (3+ months)
- Multi-language support for global teams
- Integration with HRIS systems (Workday, BambooHR)
- Advanced ML models for skill gap analysis
- Mobile app for on-the-go resource queries

## Demo

### Local Demo
1. Follow the setup instructions above
2. Start both backend and frontend services
3. Access the chat interface at http://localhost:8501

### Sample Interactions
- **Query**: "I need someone experienced with machine learning for a healthcare project"
- **Response**: AI-generated recommendations with relevant employee profiles

- **Query**: "Find developers who know both AWS and Docker"
- **Response**: Filtered list of DevOps engineers with matching skills

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, please open an issue in the GitHub repository or contact the development team.

---

**Note**: This project demonstrates modern AI-assisted development practices, combining semantic search, vector databases, and large language models to create an intelligent HR resource management system.
