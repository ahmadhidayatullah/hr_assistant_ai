"""
Core configuration module for HR Assistant AI.
"""
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "hr_database.db")
KNOWLEDGE_BASE_DIR = os.path.join(BASE_DIR, "knowledge_base")
UPLOAD_DIR = os.path.join(KNOWLEDGE_BASE_DIR, "uploads")
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore", "faiss_index")

# --- Model Configuration ---
DEFAULT_LLM_MODEL = "gemini-2.5-flash"
AVAILABLE_MODELS = [
    "gemini-3.6-flash",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
]
EMBEDDING_MODEL = "gemini-embedding-001"
FALLBACK_EMBEDDING_MODELS = [
    "gemini-embedding-001",
    "embedding-001",
    "text-embedding-004",
]
LLM_TEMPERATURE = 0.2

# --- RAG Configuration ---
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVAL_TOP_K = 3

# --- App Metadata ---
APP_TITLE = "🏢 HR Assistant AI"
APP_SUBTITLE = "PT IDELOGI INDONESIA — Asisten Cerdas untuk Kebutuhan HR Karyawan"
COMPANY_NAME = "PT IDELOGI INDONESIA"

# --- SQL Safety ---
FORBIDDEN_SQL_KEYWORDS = [
    "DROP", "DELETE", "UPDATE", "INSERT", "ALTER",
    "CREATE", "TRUNCATE", "REPLACE", "RENAME", "GRANT", "REVOKE",
]

# --- File Upload ---
ALLOWED_EXTENSIONS = ["pdf", "txt", "md"]
MAX_UPLOAD_SIZE_MB = 10

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.dirname(VECTORSTORE_DIR), exist_ok=True)
