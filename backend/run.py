"""
Simple run script - Execute from backend directory
Usage: python run.py
"""
import subprocess
import sys
import os

# Use active Python or project venv Python
def get_python_exe():
    # If already running in a venv, use that
    if hasattr(sys, 'real_prefix') or (sys.base_prefix != sys.prefix):
        return sys.executable

    backend_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.normpath(os.path.join(backend_dir, ".."))

    # Prefer repository root .venv (common setup)
    root_venv_python = os.path.join(project_root, ".venv", "Scripts", "python.exe")
    if os.path.exists(root_venv_python):
        return root_venv_python

    # Fallback: backend-local .venv
    local_venv_python = os.path.join(backend_dir, ".venv", "Scripts", "python.exe")
    if os.path.exists(local_venv_python):
        return local_venv_python
    
    # Fallback to current sys.executable
    return sys.executable

venv_python = get_python_exe()

print("🚀 Starting Pothole Detection Backend...")
print("📍 Server will be at: http://localhost:8000")
print("📖 API Docs at: http://localhost:8000/docs\n")
print(f"🐍 Using Python: {venv_python}")

backend_dir = os.path.dirname(os.path.abspath(__file__))

# Run uvicorn using detected Python
try:
    subprocess.run([
        venv_python, "-m", "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ], cwd=backend_dir, check=True)
except subprocess.CalledProcessError as exc:
    print(f"\n❌ Backend failed to start (exit code: {exc.returncode}).")
    print("If this is the first run, install dependencies with:")
    print("  ..\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt")
    raise
