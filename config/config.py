# ragex/config/config.py

import os
from dotenv import load_dotenv

# ✅ Get the path to the .env file in the same directory
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

# ✅ Load environment variables from the .env file
load_dotenv(dotenv_path)

# ✅ Access the environment variables
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
MISTRAL_LOCAL_PATH = os.getenv("MISTRAL_LOCAL_PATH")
