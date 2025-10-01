"""
Configuration file for AIResume project.
Loads environment variables and manages application settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project paths
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
BACKEND_DIR = BASE_DIR / "backend"

# Ensure upload directory exists
UPLOAD_DIR.mkdir(exist_ok=True)

# API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Default LLM model (GPT-4o: good balance of quality and cost)
DEFAULT_MODEL = "openai/gpt-4o"

# Alternative models with cost information
ALTERNATIVE_MODELS = [
    {
        "id": "openai/gpt-4o",
        "name": "GPT-4o (Recommended)",
        "cost": "~$0.04/resume",
        "description": "Good balance of quality and cost"
    },
    {
        "id": "openai/gpt-3.5-turbo",
        "name": "GPT-3.5 Turbo",
        "cost": "~$0.01/resume",
        "description": "Cheapest, best at following exact instructions"
    },
    {
        "id": "anthropic/claude-3.5-sonnet",
        "name": "Claude 3.5 Sonnet",
        "cost": "~$0.05/resume",
        "description": "Creative, sometimes uses placeholders"
    },
    {
        "id": "openai/gpt-4-turbo",
        "name": "GPT-4 Turbo",
        "cost": "~$0.10/resume",
        "description": "Best quality, most expensive"
    },
    {
        "id": "meta-llama/llama-3.1-70b-instruct",
        "name": "LLaMA 3.1 70B",
        "cost": "~$0.005/resume",
        "description": "Cheapest, variable quality"
    }
]

# Model IDs only (for backward compatibility)
MODEL_IDS = [model["id"] for model in ALTERNATIVE_MODELS]

# Resume processing settings
MAX_PROJECTS_TO_TAILOR = 2  # Tailor only the most recent 1-2 projects
BULLET_VARIATION_ALLOWED = 1  # Allow +1 or -1 bullet points
TARGET_MATCH_SCORE_MIN = 77  # Minimum target match score %
TARGET_MATCH_SCORE_MAX = 95  # Maximum realistic match score %

# File upload settings
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
MAX_FILE_SIZE_MB = 10

def validate_config():
    """Validate that required configuration is present."""
    if not OPENROUTER_API_KEY:
        raise ValueError(
            "OPENROUTER_API_KEY not found in environment variables. "
            "Please ensure .env file exists with OPENROUTER_API_KEY set."
        )
    return True
