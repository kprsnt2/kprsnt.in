"""
AI Model Configuration (Scripts Bridge)
Canonical configurations are defined in api/ai_config.py.
This module re-exports from api.ai_config to eliminate configuration drift.
"""
import os
import sys
from pathlib import Path

# Ensure repo root is in sys.path to import api.ai_config
_repo_root = Path(__file__).resolve().parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

try:
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
except ImportError:
    # Standalone fallback if api module cannot be imported
    from openai import OpenAI

    LLM_TIMEOUT = float(os.environ.get("AI_LLM_TIMEOUT", "8.0"))
    NVIDIA_MODEL = "nvidia/nemotron-3-ultra-550b-a55b"
    NVIDIA_FALLBACK_MODELS = [
        "stepfun-ai/step-3.7-flash",
        "z-ai/glm-5.1",
    ]
    NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
    NVIDIA_EMBEDDING_MODEL = "nvidia/nv-embedqa-e5-v5"

    GROQ_MODEL = "groq/compound"
    GROQ_FALLBACK_MODELS = [
        "groq/compound-mini",
        "openai/gpt-oss-120b",
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
    ]
    GROQ_BASE_URL = "https://api.groq.com/openai/v1"

    OPENAI_MODEL = "gpt-5.4-mini"
    OPENAI_MODEL_PREMIUM = NVIDIA_MODEL
    OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"

    def get_nvidia_client(timeout=None):
        api_key = os.environ.get("NVIDIA_API_KEY")
        if not api_key:
            return None
        return OpenAI(api_key=api_key, base_url=NVIDIA_BASE_URL, timeout=timeout or LLM_TIMEOUT)

    def get_groq_client(timeout=None):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return None
        return OpenAI(api_key=api_key, base_url=GROQ_BASE_URL, timeout=timeout or LLM_TIMEOUT)

    def get_openai_client(timeout=None):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return None
        return OpenAI(api_key=api_key, max_retries=0, timeout=timeout or LLM_TIMEOUT)

    def call_llm(prompt, system_prompt=None, json_mode=False, temperature=0.7, model=None, timeout=None):
        effective_timeout = timeout or LLM_TIMEOUT
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

        openai = get_openai_client(timeout=effective_timeout)
        if openai:
            try:
                r = openai.chat.completions.create(model=OPENAI_MODEL, timeout=effective_timeout, **kwargs)
                return r.choices[0].message.content
            except Exception as e:
                print(f"[OpenAI] Failed: {e}")

        nvidia = get_nvidia_client(timeout=effective_timeout)
        if nvidia:
            for m in [model or NVIDIA_MODEL] + NVIDIA_FALLBACK_MODELS:
                try:
                    r = nvidia.chat.completions.create(model=m, timeout=effective_timeout, **kwargs)
                    return r.choices[0].message.content
                except Exception as e:
                    print(f"[NVIDIA {m}] Failed: {e}")

        groq = get_groq_client(timeout=effective_timeout)
        if groq:
            for m in [GROQ_MODEL] + GROQ_FALLBACK_MODELS:
                try:
                    r = groq.chat.completions.create(model=m, timeout=effective_timeout, **kwargs)
                    return r.choices[0].message.content
                except Exception as e:
                    print(f"[Groq {m}] Failed: {e}")

        return None

    def call_llm_with_history(messages, system_prompt=None, json_mode=False, temperature=0.7, model=None, tools=None, tool_choice=None, timeout=None):
        effective_timeout = timeout or LLM_TIMEOUT
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

        openai = get_openai_client(timeout=effective_timeout)
        if openai:
            try:
                return openai.chat.completions.create(model=OPENAI_MODEL, timeout=effective_timeout, **kwargs)
            except Exception as e:
                print(f"[OpenAI] Failed: {e}")

        nvidia = get_nvidia_client(timeout=effective_timeout)
        if nvidia:
            for m in [model or NVIDIA_MODEL] + NVIDIA_FALLBACK_MODELS:
                try:
                    return nvidia.chat.completions.create(model=m, timeout=effective_timeout, **kwargs)
                except Exception as e:
                    print(f"[NVIDIA {m}] Failed: {e}")

        groq = get_groq_client(timeout=effective_timeout)
        if groq:
            groq_kwargs = {k: v for k, v in kwargs.items() if k not in ('tools', 'tool_choice')}
            for m in [GROQ_MODEL] + GROQ_FALLBACK_MODELS:
                try:
                    return groq.chat.completions.create(model=m, timeout=effective_timeout, **groq_kwargs)
                except Exception as e:
                    print(f"[Groq {m}] Failed: {e}")

        return None

    def get_embedding(text, timeout=None):
        effective_timeout = timeout or LLM_TIMEOUT
        openai = get_openai_client(timeout=effective_timeout)
        if openai:
            try:
                r = openai.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=text, timeout=effective_timeout)
                return r.data[0].embedding
            except Exception as e:
                print(f"[OpenAI Embedding] Failed: {e}")

        nvidia = get_nvidia_client(timeout=effective_timeout)
        if nvidia:
            try:
                r = nvidia.embeddings.create(model=NVIDIA_EMBEDDING_MODEL, input=text, timeout=effective_timeout)
                return r.data[0].embedding
            except Exception as e:
                print(f"[NVIDIA Embedding] Failed: {e}")

        return None
