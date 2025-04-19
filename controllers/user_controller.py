import sys
import os

# Use direct relative import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.user_model import User

def login(username, password):
    user = User.get_user(username)
    if user and user["password"] == password:
        return True, user
    return False, None

def update_status(user_id, status):
    return User.update_status(user_id, status)