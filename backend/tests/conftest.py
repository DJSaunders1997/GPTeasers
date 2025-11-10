import os
import sys

# Add backend directory explicitly
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))  # Add tests directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # Add backend directory
