
import os
import sys
import subprocess


os.chdir(os.path.join(os.path.dirname(__file__), 'frontend'))

if __name__ == "__main__":
    print("Starting HR Resource Bot Frontend...")
    print("Frontend will be available at: http://localhost:8501")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    
    subprocess.run(["streamlit", "run", "streamlit_app.py"])
