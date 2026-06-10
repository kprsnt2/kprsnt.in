"""
AI Model Configuration for API endpoints
Change model names here to switch providers/models across all API functions.
"""
import os
from openai import OpenAI

# ============================================
# MODEL NAMES — Change these to switch models
# ============================================

# Primary: NVIDIA (via OpenAI-compatible API)
NVIDIA_MODEL = "nvidia/nemotron-3-ultra-550b-a55b"
NVIDIA_FALLBACK_MODELS = [
    "stepfun-ai/step-3.7-flash",
    "z-ai/glm-5.1",
]
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
NVIDIA_EMBEDDING_MODEL = "nvidia/nv-embedqa-e5-v5"

# Backup: Groq (via OpenAI-compatible API)
GROQ_MODEL = "openai/gpt-oss-120b"
GROQ_FALLBACK_MODELS = [
    "groq/compound",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
]
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# Last resort: OpenAI (requires positive credit balance)
OPENAI_MODEL = "gpt-5.4-mini"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


# ============================================
# CLIENT FACTORIES
# ============================================

def get_nvidia_client():
    """Get the NVIDIA primary client."""
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key, base_url=NVIDIA_BASE_URL)


def get_groq_client():
    """Get the Groq backup client."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key, base_url=GROQ_BASE_URL)


def get_openai_client():
    """Get the OpenAI last-resort client (no retries to fail fast)."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key, max_retries=0)


# ============================================
# LLM CALL HELPERS
# ============================================

def call_llm(prompt, system_prompt=None, json_mode=False, temperature=0.7, model=None):
    """Call LLM: NVIDIA → Groq → OpenAI fallback chain."""
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    kwargs = {
        "messages": messages,
        "temperature": temperature,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    # 1. NVIDIA (primary)
    nvidia = get_nvidia_client()
    if nvidia:
        for m in [model or NVIDIA_MODEL] + NVIDIA_FALLBACK_MODELS:
            try:
                r = nvidia.chat.completions.create(model=m, **kwargs)
                return r.choices[0].message.content
            except Exception as e:
                print(f"[NVIDIA {m}] Failed: {e}")

    # 2. Groq (backup)
    groq = get_groq_client()
    if groq:
        for m in [GROQ_MODEL] + GROQ_FALLBACK_MODELS:
            try:
                r = groq.chat.completions.create(model=m, **kwargs)
                return r.choices[0].message.content
            except Exception as e:
                print(f"[Groq {m}] Failed: {e}")

    # 3. OpenAI (last resort — needs credits)
    openai = get_openai_client()
    if openai:
        try:
            r = openai.chat.completions.create(model=OPENAI_MODEL, **kwargs)
            return r.choices[0].message.content
        except Exception as e:
            print(f"[OpenAI] Failed: {e}")

    return None


def call_llm_with_history(messages, system_prompt=None, json_mode=False, temperature=0.7, model=None, tools=None, tool_choice=None):
    """Call LLM with full message history (for chat). NVIDIA → Groq → OpenAI."""
    full_messages = []
    if system_prompt:
        full_messages.append({"role": "system", "content": system_prompt})
    full_messages.extend(messages)

    kwargs = {
        "messages": full_messages,
        "temperature": temperature,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    if tools:
        kwargs["tools"] = tools
    if tool_choice:
        kwargs["tool_choice"] = tool_choice

    # 1. NVIDIA (primary — supports function calling)
    nvidia = get_nvidia_client()
    if nvidia:
        for m in [model or NVIDIA_MODEL] + NVIDIA_FALLBACK_MODELS:
            try:
                return nvidia.chat.completions.create(model=m, **kwargs)
            except Exception as e:
                print(f"[NVIDIA {m}] Failed: {e}")

    # 2. Groq (backup — drop tools if not supported)
    groq = get_groq_client()
    if groq:
        groq_kwargs = {k: v for k, v in kwargs.items() if k not in ('tools', 'tool_choice')}
        for m in [GROQ_MODEL] + GROQ_FALLBACK_MODELS:
            try:
                return groq.chat.completions.create(model=m, **groq_kwargs)
            except Exception as e:
                print(f"[Groq {m}] Failed: {e}")

    # 3. OpenAI (last resort)
    openai = get_openai_client()
    if openai:
        try:
            return openai.chat.completions.create(model=OPENAI_MODEL, **kwargs)
        except Exception as e:
            print(f"[OpenAI] Failed: {e}")

    return None


# ============================================
# EMBEDDINGS
# ============================================

def get_embedding(text):
    """Get embedding vector. NVIDIA → OpenAI fallback."""
    # 1. NVIDIA embeddings (primary)
    nvidia = get_nvidia_client()
    if nvidia:
        try:
            r = nvidia.embeddings.create(model=NVIDIA_EMBEDDING_MODEL, input=text)
            return r.data[0].embedding
        except Exception as e:
            print(f"[NVIDIA Embedding] Failed: {e}")

    # 2. OpenAI embeddings (fallback — needs credits)
    openai = get_openai_client()
    if openai:
        try:
            r = openai.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=text)
            return r.data[0].embedding
        except Exception as e:
            print(f"[OpenAI Embedding] Failed: {e}")

    return None
