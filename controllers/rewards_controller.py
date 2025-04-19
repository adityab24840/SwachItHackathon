import sys
import os

# Use direct relative import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.rewards_model import Rewards

def get_user_rewards(user_id):
    return Rewards.get_rewards(user_id)