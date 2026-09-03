import os
import json
import logging
from typing import Dict, Any, List

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
    else:
        skill = _load_skill("interview")
        portfolio_context = get_interview_context()

    # 2. Load live pipeline data (jobs, brands, pharma)
    live_data = get_all_live_data()

    # 3. Build the system prompt: skill instructions + portfolio + live data
    prompt = skill + "\n\n"
    prompt += "## Portfolio Data\n" + portfolio_context + "\n"
    if live_data:
        prompt += "\n## Live Pipeline Data (real-time)\n" + live_data + "\n"

    return prompt

try:
    from ai_config import call_llm_with_history, OPENAI_MODEL
except ImportError:
    from .ai_config import call_llm_with_history, OPENAI_MODEL


# OpenAI function calling tool definition for send_resume_to_user
RESUME_TOOL = {
    "type": "function",
    "function": {
        "name": "send_resume_to_user",
        "description": "Sends Prashanth's resume to the specified email address. Use this when the user asks to receive a resume or CV via email.",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "The email address to send the resume to."
                }
            },
            "required": ["email"]
        }
    }
}


def send_resume_to_user(email: str) -> str:
    """Sends Prashanth's resume to the specified email address.
    
    Args:
        email (str): The email address to send the resume to.
    """
    logger.info(f"Tool called: send_resume_to_user({email})")
    try:
        import resend
        resend.api_key = os.environ.get("RESEND_API_KEY")
        if not resend.api_key:
            return "Failed: RESEND_API_KEY not configured"
            
        from_email = os.environ.get("INTERVIEW_FROM_EMAIL", "chat@kprsnt.in")
        
        resend.Emails.send({
            "from": f"Prashanth Kumar Kadasi <{from_email}>",
            "to": [email],
            "subject": "Prashanth Kumar Kadasi - Resume",
            "html": f"""<div style="font-family: -apple-system, sans-serif; padding: 20px;">
                <p>Hi there,</p>
                <p>As requested, here is a link to my latest resume and portfolio:</p>
                <p><a href="https://kprsnt.in/resume" style="display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px;">View Resume Online</a></p>
                <p>Best,<br>Prashanth</p>
            </div>"""
        })
        return f"Successfully sent resume to {email}"
    except Exception as e:
        logger.error(f"Error sending resume: {e}")
        return f"Failed to send resume: {str(e)}"


# Map of available tool functions for dispatching
_TOOL_FUNCTIONS = {
    "send_resume_to_user": send_resume_to_user,
}


def get_ai_response(message: str, agent_type: str = "interview", history: List[Dict[str, str]] = None) -> str:
    """Get AI response using OpenAI (primary) with NVIDIA fallback, via ai_config."""
    try:
        system_prompt = get_system_prompt(agent_type)
        
        # Build OpenAI-format message history
        messages = []
        if history and len(history) > 0:
            for item in history:
                role = item.get("role", "user")
                if role == "model":
                    role = "assistant"
                content = item.get("content", item.get("parts", ""))
                messages.append({"role": role, "content": content})
        
        # Add the current user message
        messages.append({"role": "user", "content": message})
        
        # Call LLM with tools (function calling)
        response = call_llm_with_history(
            messages,
            system_prompt=system_prompt,
            tools=[RESUME_TOOL],
            temperature=0.7,
        )
        
        if response is None:
            return "I'm sorry, my AI service is temporarily unavailable. Please try again later."
        
        response_message = response.choices[0].message
        
        # Handle tool calls (function calling) — loop until the model produces a text reply
        max_tool_rounds = 3
        for _ in range(max_tool_rounds):
            if not response_message.tool_calls:
                break
            
            # Append the assistant message with tool_calls to history
            messages.append(response_message)
            
            # Execute each tool call and add results
            for tool_call in response_message.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)
                
                fn = _TOOL_FUNCTIONS.get(fn_name)
                if fn:
                    result = fn(**fn_args)
                else:
                    result = f"Unknown function: {fn_name}"
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                })
            
            # Call the model again with tool results
            response = call_llm_with_history(
                messages,
                system_prompt=system_prompt,
                tools=[RESUME_TOOL],
                temperature=0.7,
            )
            
            if response is None:
                return "I'm sorry, something went wrong processing your request."
            
            response_message = response.choices[0].message
        
        text = response_message.content or ""
        return text.replace('**', '').replace('*', '')
        
    except Exception as e:
        import traceback
        logger.error(f"AI API error: {traceback.format_exc()}")
        return "I'm sorry, something went wrong. Please try again later."


# Backward-compatible alias so existing imports keep working
get_gemini_response = get_ai_response


def send_reply_email(to_email: str, subject: str, body: str, agent_type: str = "interview") -> bool:
    """Send reply email via Resend API."""
    try:
        import resend
        
        resend.api_key = os.environ.get("RESEND_API_KEY")
        if not resend.api_key:
            return False
            
        sender = "Rash Agent" if agent_type == "interview" else "RashBot"
        from_email = os.environ.get("INTERVIEW_FROM_EMAIL", f"{agent_type}@kprsnt.in")
        
        resend.Emails.send({
            "from": f"{sender} <{from_email}>",
            "to": [to_email],
            "subject": f"Re: {subject}" if not subject.startswith("Re:") else subject,
            "text": body,
            "html": f"""<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="white-space: pre-wrap; line-height: 1.6; color: #333;">{body}</div>
                <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 24px 0;">
                <div style="font-size: 12px; color: #888;">
                    <p>🤖 This reply was generated by <b>{sender}</b>.</p>
                    <p>Portfolio: <a href="https://kprsnt.in" style="color: #667eea;">kprsnt.in</a></p>
                </div>
            </div>"""
        })
        return True
    except Exception as e:
        logger.error(f"Resend send error: {e}")
        return False

def notify_owner(from_email: str, message: str, ai_response: str, source: str = "API", agent_type: str = "interview"):
    """Send a notification to the owner."""
    try:
        import resend
        resend.api_key = os.environ.get("RESEND_API_KEY")
        if not resend.api_key: return
        
        owner_email = os.environ.get("OWNER_NOTIFY_EMAIL")
        if not owner_email: return
        
        bot_name = "Rash Agent" if agent_type == "interview" else "RashBot"
        from_email_addr = os.environ.get("INTERVIEW_FROM_EMAIL", f"{agent_type}@kprsnt.in")
        
        resend.Emails.send({
            "from": f"{bot_name} Notifications <{from_email_addr}>",
            "to": [owner_email],
            "subject": f"🔔 {bot_name} Used — {from_email or 'Anonymous'}",
            "html": f"""<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <h3 style="color: #667eea; margin-top: 0;">🔔 Someone interacted with {bot_name}</h3>
                <p><b>Source:</b> {source}<br><b>From:</b> {from_email or 'Web Viewer'}</p>
                <div style="background: #f5f5f5; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
                    <p style="margin: 0 0 4px; font-weight: bold;">User said:</p>
                    <p style="margin: 0;">{message}</p>
                </div>
                <div style="background: #eef2ff; border-radius: 8px; padding: 16px;">
                    <p style="margin: 0 0 4px; font-weight: bold;">{bot_name} said:</p>
                    <p style="margin: 0; white-space: pre-wrap;">{ai_response}</p>
                </div>
            </div>"""
        })
    except Exception as e:
        logger.error(f"Resend notification error: {e}")
