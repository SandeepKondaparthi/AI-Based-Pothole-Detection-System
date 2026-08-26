import os
import subprocess
import sys
import shutil
from pathlib import Path
import platform

# Project Configuration
ROOT_DIR = Path(__file__).parent.absolute()
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"

# Utility for printing status
def print_status(message, status="info"):
    colors = {
        "info": "\033[94m[*]\033[0m",
        "success": "\033[92m[+]\033[0m",
        "warning": "\033[93m[!]\033[0m",
        "error": "\033[91m[X]\033[0m"
    }
    # Reset colors for Windows if needed, though modern terminals support ANSI
    if platform.system() == "Windows":
        os.system("") # Enable ANSI escape codes
    
    print(f"{colors.get(status, '[*]')} {message}")

def run_command(command, cwd=None, env=None):
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def cleanup():
    print_status("Starting scoped cleanup...", "info")
    
    targets = [
        BACKEND_DIR / "venv",
        BACKEND_DIR / ".venv",
        FRONTEND_DIR / "node_modules",
        FRONTEND_DIR / "dist",
        ROOT_DIR / ".pytest_cache"
    ]
    
    for target in targets:
        if target.exists():
            print_status(f"Removing {target.relative_to(ROOT_DIR)}...", "info")
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
    
    # Clean __pycache__
    for pycache in ROOT_DIR.rglob("__pycache__"):
        if ".venv" not in str(pycache) and "venv" not in str(pycache):
            print_status(f"Removing {pycache.relative_to(ROOT_DIR)}...", "info")
            shutil.rmtree(pycache)

def setup_backend():
    print_status("Setting up Backend (FastAPI)...", "info")
    venv_dir = BACKEND_DIR / ".venv"
    
    # Create venv
    print_status("Creating virtual environment...", "info")
    success, output = run_command(f"{sys.executable} -m venv .venv", cwd=BACKEND_DIR)
    if not success:
        print_status(f"Failed to create venv: {output}", "error")
        return False

    # Pip path
    pip_exe = venv_dir / "Scripts" / "pip.exe" if platform.system() == "Windows" else venv_dir / "bin" / "pip"
    
    # Install dependencies
    reqs = BACKEND_DIR / "requirements.txt"
    if reqs.exists():
        print_status("Installing backend dependencies...", "info")
        success, output = run_command(f'"{pip_exe}" install -r requirements.txt', cwd=BACKEND_DIR)
        if not success:
            print_status(f"Failed to install dependencies: {output}", "error")
            return False
    
    # Install dev dependencies
    reqs_dev = BACKEND_DIR / "requirements-dev.txt"
    if reqs_dev.exists():
        print_status("Installing backend dev dependencies...", "info")
        success, output = run_command(f'"{pip_exe}" install -r requirements-dev.txt', cwd=BACKEND_DIR)
        if not success:
            print_status(f"Failed to install dev dependencies: {output}", "error")
            return False
            
    print_status("Backend setup completed.", "success")
    return True

def setup_frontend():
    print_status("Setting up Frontend (React + Vite)...", "info")
    
    # Check if npm is installed
    success, output = run_command("npm --version")
    if not success:
        print_status("NPM not found. Please install Node.js.", "error")
        return False

    lock_file = FRONTEND_DIR / "package-lock.json"
    cmd = "npm ci" if lock_file.exists() else "npm install"
    
    print_status(f"Running '{cmd}'...", "info")
    success, output = run_command(cmd, cwd=FRONTEND_DIR)
    if not success:
        print_status(f"Failed to install frontend dependencies: {output}", "error")
        return False
        
    print_status("Frontend setup completed.", "success")
    return True

def validate():
    print_status("Validating environment...", "info")
    
    # Check .env files
    for entry in [BACKEND_DIR / ".env", FRONTEND_DIR / ".env"]:
        if not entry.exists():
            example = entry.parent / ".env.example"
            if example.exists():
                print_status(f"Creating {entry.name} from example...", "warning")
                shutil.copy(example, entry)
            else:
                print_status(f"Missing {entry.name} and {example.name}!", "error")
    
    # Check upload directory
    upload_dir = BACKEND_DIR / "uploads"
    if not upload_dir.exists():
        print_status("Creating uploads directory...", "info")
        upload_dir.mkdir(parents=True, exist_ok=True)

    print_status("Validation completed.", "success")

def main():
    print_status("="*40)
    print_status("RoadCare Environment Setup Automation")
    print_status("="*40)
    
    cleanup()
    
    backend_success = setup_backend()
    frontend_success = setup_frontend()
    
    validate()
    
    print_status("="*40)
    if backend_success and frontend_success:
        print_status("Setup completed successfully!", "success")
        print_status("You can now start the servers using start-dev.bat", "info")
    else:
        print_status("Setup completed with errors. Please check the logs above.", "error")
    print_status("="*40)

if __name__ == "__main__":
    main()
