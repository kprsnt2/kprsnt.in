"""
AI Model Configuration (Scripts Bridge)
Canonical configurations are defined in api/ai_config.py.
This module re-exports from api.ai_config to eliminate configuration drift.
"""
import sys
from pathlib import Path

# Ensure repo root is in sys.path to import api.ai_config
_repo_root = Path(__file__).resolve().parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

# Single-source config (audit L15): every value and client factory comes
# from api/ai_config.py. The repo root is on sys.path above, so standalone
# script runs still work; a genuinely missing dependency now fails loudly
# instead of silently running a stale duplicate of this config.
from api.ai_config import (
    NVIDIA_MODEL,
    NVIDIA_FALLBACK_MODELS,
    NVIDIA_BASE_URL,
    NVIDIA_EMBEDDING_MODEL,
    GROQ_MODEL,
    GROQ_FALLBACK_MODELS,
    GROQ_BASE_URL,
    OPENAI_MODEL,
    OPENAI_MODEL_PREMIUM,
    OPENAI_EMBEDDING_MODEL,
    LLM_TIMEOUT,
    get_nvidia_client,
    get_groq_client,
    get_openai_client,
    call_llm,
    call_llm_with_history,
    get_embedding,
)

# Re-export contract: consumers import these names from scripts.ai_config.
__all__ = [
    "NVIDIA_MODEL",
    "NVIDIA_FALLBACK_MODELS",
    "NVIDIA_BASE_URL",
    "NVIDIA_EMBEDDING_MODEL",
    "GROQ_MODEL",
    "GROQ_FALLBACK_MODELS",
    "GROQ_BASE_URL",
    "OPENAI_MODEL",
    "OPENAI_MODEL_PREMIUM",
    "OPENAI_EMBEDDING_MODEL",
    "LLM_TIMEOUT",
    "get_nvidia_client",
    "get_groq_client",
    "get_openai_client",
    "call_llm",
    "call_llm_with_history",
    "get_embedding",
]
