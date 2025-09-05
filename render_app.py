import sys
from pathlib import Path

# Point Python to the backend folder
backend_dir = Path(__file__).parent / "airfoil-backend"
sys.path.insert(0, str(backend_dir))

# Import the Flask app directly from src/main.py
from src import main

app = main.app
