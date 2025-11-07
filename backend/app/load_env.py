# app/load_env.py
import os
from dotenv import load_dotenv

def ensure_env_loaded():
    """Guarantee .env variables are always available app-wide"""
    env_path = os.path.join(os.getcwd(), '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path, override=True)
    else:
        print("⚠️ .env file not found at:", env_path)
