"""
AI Model Configuration for API endpoints
Change model names here to switch providers/models across all API functions.
"""
import os
from openai import OpenAI

# ============================================
# MODEL NAMES — Change these to switch models
# ============================================
OPENAI_MODEL = "gpt-5.4-mini"                      # Default model
OPENAI_MODEL_PREMIUM = "gpt-5.4"                    # Premium model (for ai-insight)
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"   # Embedding model

# NVIDIA Fallback (OpenAI-compatible API)
NVIDIA_MODEL = "nvidia/nemotron-3-ultra-550b-a55b"  # Primary NVIDIA model
NVIDIA_FALLBACK_MODELS = [
    "stepfun-ai/step-3.7-flash",
    "z-ai/glm-5.1",
]
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"


def get_openai_client():
    """Get the primary OpenAI client."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def get_nvidia_client():
    """Get the NVIDIA fallback client (OpenAI-compatible)."""
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key, base_url=NVIDIA_BASE_URL)


def call_llm(prompt, system_prompt=None, json_mode=False, temperature=0.7, model=None):
    """Call LLM with OpenAI primary and NVIDIA fallback."""
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
    
    # Try OpenAI first
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model=model or OPENAI_MODEL,
            **kwargs
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[OpenAI] Failed: {e}")
    
    # Try NVIDIA fallback
    nvidia_client = get_nvidia_client()
    if nvidia_client:
        for nvidia_model in [NVIDIA_MODEL] + NVIDIA_FALLBACK_MODELS:
            try:
                response = nvidia_client.chat.completions.create(
                    model=nvidia_model,
                    **kwargs
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"[NVIDIA {nvidia_model}] Failed: {e}")
    
    return None


def call_llm_with_history(messages, system_prompt=None, json_mode=False, temperature=0.7, model=None, tools=None, tool_choice=None):
    """Call LLM with full message history (for chat). OpenAI primary, NVIDIA fallback."""
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
    
    # Try OpenAI first
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model=model or OPENAI_MODEL,
            **kwargs
        )
        return response
    except Exception as e:
        print(f"[OpenAI] Failed: {e}")
    
    # Try NVIDIA fallback (remove tools if not supported)
    nvidia_client = get_nvidia_client()
    if nvidia_client:
        nvidia_kwargs = {k: v for k, v in kwargs.items() if k not in ('tools', 'tool_choice')}
        for nvidia_model in [NVIDIA_MODEL] + NVIDIA_FALLBACK_MODELS:
            try:
                response = nvidia_client.chat.completions.create(
                    model=nvidia_model,
                    **nvidia_kwargs
                )
                return response
            except Exception as e:
                print(f"[NVIDIA {nvidia_model}] Failed: {e}")
    
    return None


def get_embedding(text):
    """Get embedding vector using OpenAI."""
    client = get_openai_client()
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding
