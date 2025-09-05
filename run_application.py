#!/usr/bin/env python3
"""
Standalone Airfoil Generator Application
Run this script to start the web application locally
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        sys.exit(1)

def install_dependencies():
    """Install required Python packages"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "flask", "flask-cors", "numpy", "flask-sqlalchemy"
        ])
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("Error installing dependencies. Please install manually:")
        print("pip install flask flask-cors numpy flask-sqlalchemy")
        sys.exit(1)

def start_application():
    """Start the Flask application"""
    current_dir = Path(__file__).parent
    backend_dir = current_dir / "airfoil-backend"
    
    if not backend_dir.exists():
        print("Error: airfoil-backend directory not found!")
        print("Please make sure you've extracted all files correctly.")
        sys.exit(1)
        
    # Add backend_dir to Python path
    sys.path.insert(0, str(backend_dir))
    
    print("Starting Airfoil Generator Application...")
    print("The application will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    # Import and run the Flask app
    try:
        from src.main import app
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://localhost:5000')
        
        import threading
        threading.Thread(target=open_browser, daemon=True).start()
        
        # Start the Flask app
        app.run(host='0.0.0.0', port=5000, debug=False)
        
    except ImportError as e:
        print(f"Error importing application: {e}")
        print("Please check that all files are present and dependencies are installed.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nApplication stopped.")
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 50)
    print("Airfoil Coordinate Generator")
    print("=" * 50)
    
    check_python_version()
    
    # Ask user if they want to install dependencies
    install_deps = input("Install/update dependencies? (y/n): ").lower().strip()
    if install_deps in ['y', 'yes', '']:
        install_dependencies()
    
    start_application()