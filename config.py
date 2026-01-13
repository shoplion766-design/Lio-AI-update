from dotenv import load_dotenv
import os

load_dotenv()

HOST = "0.0.0.0"
PORT = 5000
DEBUG = True
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AGENT_API_KEY = os.getenv("AGENT_API_KEY")
MAX_TOKENS = 800
