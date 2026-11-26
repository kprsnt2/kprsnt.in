import logging
import os
from typing import Dict, List

logger = logging.getLogger(__name__)

try:
    from data.portfolio_kb import get_interview_context, get_chat_context
except ImportError:
    from api.data.portfolio_kb import get_interview_context, get_chat_context

try:
    from services.live_data import get_all_live_data
except ImportError:
    from api.services.live_data import get_all_live_data


def _load_skill(skill_name: str) -> str:
    """Load a skill.md file from api/skills/ directory."""
    skill_path = os.path.join(os.path.dirname(__file__), 'skills', f'{skill_name}.md')
    try:
        with open(skill_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.warning(f"Could not load skill {skill_name}: {e}")
        return ""


def get_system_prompt(agent_type: str = "interview") -> str:
    """Generate the system prompt from skill files + portfolio KB + live data."""

    # 1. Load the skill file (defines bot personality and rules)
    if agent_type == "chat":
        skill = _load_skill("chat")
        portfolio_context = get_chat_context()
    elif agent_type == "ecosystem":
        skill = _load_skill("ecosystem")
        portfolio_context = get_interview_context()
    elif agent_type in ("rash", "alter-ego"):
        skill = _load_skill("rash")
        portfolio_context = get_chat_context()
    elif agent_type in ("cosmic", "universe"):
        skill = _load_skill("cosmic")
        portfolio_context = ""
    elif agent_type in ("critic", "bar-raiser"):
        skill = _load_skill("critic")
        portfolio_context = ""
    elif agent_type in ("pruner", "ponytail", "ponytail-review", "ponytail-audit", "ponytail-debt"):
        skill_name = "pruner" if agent_type == "pruner" else agent_type
        skill = _load_skill(skill_name)
        portfolio_context = ""
    else:
        skill = _load_skill("interview")
        portfolio_context = get_interview_context()
    # 2. Build system prompt: include portfolio context if present
    prompt = skill.strip() + "\n\n"
    if portfolio_context:
        prompt += "## Portfolio Data\n" + portfolio_context + "\n"

    # 3. Load live pipeline data strictly for visitor, interview, and alter-ego agents
    if agent_type in ("interview", "chat", "ecosystem", "rash", "alter-ego"):
        live_data = get_all_live_data()
        if live_data:
            prompt += "\n## Live Pipeline Data (real-time)\n" + live_data + "\n"
    return prompt

try:
    from ai_config import call_llm_with_history
except ImportError:
    from .ai_config import call_llm_with_history


# The bots answer on the website and over the HTTP API only. They never send
# email themselves. Mail to interview@ / chat@kprsnt.in is answered by the
# Cloudflare Email Worker (cloudflare/email-worker/), which calls these endpoints and
# copies Prashanth on every reply.
_CONTACT_NOTE = (
    "\n\n## Contact\n"
    "You cannot send emails or files. If someone asks for the resume, give the link "
    "https://kprsnt.in/resume. If they want to reach Prashanth, schedule an interview "
    "or follow up, give the address interview@kprsnt.in, which he reads himself.\n"
)


def get_ai_response(message: str, agent_type: str = "interview", history: List[Dict[str, str]] = None) -> str:
    """Get an AI reply through the provider chain in ai_config."""
    try:
        system_prompt = get_system_prompt(agent_type) + _CONTACT_NOTE

        messages = []
        for item in history or []:
            role = item.get("role", "user")
            if role == "model":
                role = "assistant"
            messages.append({"role": role, "content": item.get("content", item.get("parts", ""))})
        messages.append({"role": "user", "content": message})

        response = call_llm_with_history(messages, system_prompt=system_prompt, temperature=0.7)
        if response is None:
            return "I'm sorry, my AI service is temporarily unavailable. Please try again later."

        text = response.choices[0].message.content or ""
        return text.replace('**', '').replace('*', '')

    except Exception:
        logger.exception("AI API error")
        return "I'm sorry, something went wrong. Please try again later."


# Backward-compatible alias so existing imports keep working
get_gemini_response = get_ai_response
