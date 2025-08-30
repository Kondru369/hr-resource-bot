
import os
import sys
import uvicorn


backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)


os.chdir(backend_dir)

if __name__ == "__main__":
    print("Starting HR Resource Bot Backend...")
    print("Backend will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
