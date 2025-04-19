import os
import sys

# Get the absolute path of the project
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the absolute path to sys.path
if project_root not in sys.path:
    sys.path.append(project_root)

# Now import using absolute path
from models.waste_model import Waste

def get_daily_waste_stats():
    return Waste.get_daily_stats()

def get_cleanliness_score():
    return Waste.get_cleanliness_score()